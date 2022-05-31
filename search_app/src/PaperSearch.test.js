import {act, render, screen} from '@testing-library/react';

import {setupServer} from "msw/node";
import {rest} from "msw";
import {PaperSearchPage} from "./PaperSearch";
import userEvent from "@testing-library/user-event";


describe("Key User Journeys", () => {

    let reading_list_json = [{
        'id': '1',
        'paper_url': 'https://doi.org/10.1016/0002-8703(80)106-100',
        'title': 'A Paper Added Historically'
    }]

    const server = setupServer(
        rest.get('http://127.0.0.1:5000/api/v1/search', (req, res, ctx) => {

            //check that search_term param contains the value provided by the user e.g. = coronavirus
            const search_term = req.url.searchParams.get('search_term')

            expect(search_term).toEqual("coronavirus")

            return res(ctx.json([{
                'abstract': 'This paper explores coronaviruses in balkan nephritis',
                'authors': 'Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta',
                'id': '1',
                'journal': 'American Heart Journal',
                'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5',
                'publish_date': '1980-03-31',
                'title': 'New Viruses in Balkan nephritis'
            }, {
                'abstract': 'This paper explores for coronaviruses',
                'authors': 'Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.',
                'id': '2',
                'journal': 'Biochemical and Biophysical Research Communications',
                'paper_url': 'https://doi.org/10.1016/0006-291x(89)90049-1',
                'publish_date': '1989-03-15',
                'title': 'Predict7, a program for protein structure prediction'
            }]))
        }),

        rest.get("http://127.0.0.1:5000/api/v1/reading_list", (req, res, ctx) => {
            return res(ctx.json(reading_list_json))
        }),

        rest.post("http://127.0.0.1:5000/api/v1/reading_list", (req, res, ctx) => {


            const request_body = req.body

            const item_title = request_body.title
            const item_url = request_body.paper_url
            //check that the item to be added contains the values from the first row in table of results
            expect(item_title).toEqual("New Viruses in Balkan nephritis")
            expect(item_url).toEqual("https://doi.org/10.1016/0002-8703(80)90355-5")

            //update our mocked store of reading list items so subsequent calls to GET /reading_list will return the correct count of items

            reading_list_json.push(request_body)

            //return the item sent to user making sure to include it's id -- API generates this id in prod
            request_body.id = "2"
            return res(ctx.json(request_body))
        })
    )


    beforeAll(() => server.listen())
    afterEach(() => server.resetHandlers())
    afterAll(() => server.close())


    test("User Can Search For Keyword And View Results", async () => {

        render(<PaperSearchPage></PaperSearchPage>)

        //User enters search term into search box and submits

        let search_button = await screen.findByRole('button', {'name': 'Search'})
        let search_box = await screen.findByRole('textbox')

        await act(() => {
            userEvent.type(search_box, "coronavirus")
            userEvent.click(search_button)
        })


        //wait until query has finished loading
        await screen.findByText("2 Results Have Been Found")

        let table_rows = await screen.findAllByRole("row")

        //Check that user can see both rows and that they contain the correct titles/publish date/journal and authors
        expect(table_rows[1]).toHaveTextContent('New Viruses in Balkan nephritis')
        expect(table_rows[2]).toHaveTextContent('Predict7, a program for protein structure prediction')

        expect(table_rows[1]).toHaveTextContent('1980-03-31')
        expect(table_rows[2]).toHaveTextContent('1989-03-15')

        expect(table_rows[1]).toHaveTextContent('American Heart Journal')
        expect(table_rows[2]).toHaveTextContent('Biochemical and Biophysical Research Communications')

        expect(table_rows[1]).toHaveTextContent('Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta')
        expect(table_rows[2]).toHaveTextContent('Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.')



    })


    test("User Can View And Add Items To Reading List", async () => {
        render(<PaperSearchPage></PaperSearchPage>)

        //User enters search term into search box and submits

        let search_button = await screen.findByRole('button', {'name': 'Search'})
        let search_box = await screen.findByRole('textbox')

        await act(() => {
            userEvent.type(search_box, "coronavirus")
            userEvent.click(search_button)
        })


        //wait until query has finished loading
        await screen.findByText("2 Results Have Been Found")

        //Check there is only 1 item in the reading list - Will throw an error if more than 1 item exists
        //Our Reading List button name actually contains a count of items added to the reading list
        let dropdown_button = await screen.findByRole("button", {name: "Reading List (1)"})


         //checks the item in the reading list is the one added historically
        await act(() => {
            userEvent.click(dropdown_button)
        })

        expect(await screen.findByTestId("Dropdown Row 1")).toHaveTextContent("A Paper Added Historically")

        //User clicks the first "add" button
        let add_buttons = await screen.findAllByRole("button", {name: "Add"})


        await act(() => {
            userEvent.click(add_buttons[0])
        })

        //The below checks there are now two items present in the Reading List
        dropdown_button = await screen.findByRole("button", {name: "Reading List (2)"})

        await act(() => {
            userEvent.click(dropdown_button)
        })

        //check that the correct titles and urls exist for each dropdown items

        let dropdown_item_1 = await screen.findByTestId("Dropdown Row 1")
        let dropdown_item_2 = await screen.findByTestId("Dropdown Row 2")

        expect(dropdown_item_1).toHaveTextContent("A Paper Added Historically")
        expect(dropdown_item_2).toHaveTextContent("New Viruses in Balkan nephritis")
        expect(dropdown_item_1.href).toBe("https://doi.org/10.1016/0002-8703(80)106-100")
        expect(dropdown_item_2.href).toBe("https://doi.org/10.1016/0002-8703(80)90355-5")


    })

})
