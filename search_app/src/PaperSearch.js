import {Container, Form, Row, Table} from "react-bootstrap";
import {useFormik} from "formik";
import {useState} from "react";

export function PaperSearchPage() {

    const [search_results, set_search_results] = useState([{
        'title': 'Coronaviruses in Balkan nephritis', 'publish_date': '1980-03-31',
        'paper_url': 'https://doi.org/10.1016/0002-8703(80)90355-5',
        'journal': 'American Heart Journal',
        'authors': 'Georgescu, Leonida; Diosi, Peter; Buţiu, Ioan; Plavoşin, Livia; Herzog, Georgeta',
        'id': '1',
        'abstract': 'This is a journal article that explores coronaviruses in balkan nephritis'
    },
        {
            'title': 'Predict7, a program for protein structure prediction',
            'publish_date': '1989-03-15', 'paper_url': 'https://doi.org/10.1016/0006-291x(89)90049-1',
            'journal': 'Biochemical and Biophysical Research Communications',
            'authors': 'Cármenes, R.S.; Freije, J.P.; Molina, M.M.; Martín, J.M.', 'id': '2',
            'abstract': 'This is a journal article that explores protein structure prediction in coronaviruses'
        }])


    return (

        <Container>
            <Row>

                <SearchBox set_search_results={set_search_results}></SearchBox>
            </Row>

            <Row>
                <ResultCounter result_count={search_results.length}></ResultCounter>
            </Row>

            <Row>
                <SearchResultTable search_results={search_results}></SearchResultTable>
            </Row>
        </Container>
    )

}


async function FetchSearchResults(search_term, set_search_results) {


    if (search_term == undefined) {

        set_search_results([])
    }

    const response = await fetch(`http://127.0.0.1:5000/api/v1/search?search_term=${search_term}`,{method:'GET'})

    try {
        if (response.ok) {
            const response_data = await response.json();
            set_search_results(response_data)
        }
    }

    catch(err){
        set_search_results([])
    }
}


function SearchBox(props) {

    const {set_search_results} = props

    const formik = useFormik({
        initialValues: {
            search_term: "",
        },
        onSubmit: values => {
            FetchSearchResults(values.search_term, set_search_results)
        }

    });

    return (
        <form onSubmit={formik.handleSubmit}>
            <label htmlFor="search_term">Search Input</label>
            <input id={"search_term"} name={"search_term"} type="search_term"
                   onChange={formik.handleChange} value={formik.values.search_term}/>
            <button type={"submit"}>Search</button>

        </form>
    )

}

function ResultCounter(props) {

    const {result_count} = props


    if (result_count === 1) {
        return <div> 1 Result Has Been Found</div>
    }
    return (<div>{result_count} Results Have Been Found</div>)
}

function SearchResultRow(props) {

    const {search_result} = props
    const {title} = search_result
    const {publish_date} = search_result
    const {journal} = search_result
    const {authors} = search_result
    const {paper_url} = search_result

    return (
        <tr>
            <td>
                <a href={paper_url}>{title}</a>
            </td>

            <td>
                {publish_date}
            </td>

            <td>
                {journal}
            </td>

            <td>
                {authors}
            </td>
        </tr>
    )

}


function SearchResultTable(props) {

    const {search_results} = props


    const table_rows = search_results.map((search_result) => {
        return <SearchResultRow key={search_result.id} search_result={search_result}></SearchResultRow>
    })


    return (
        <Table striped bordered hover size={"sm"}>
            <thead>
            <tr>
                <th>Title</th>
                <th>Publish Date</th>
                <th>Journal</th>
                <th>Authors</th>
            </tr>

            </thead>

            <tbody>
            {table_rows}
            </tbody>

        </Table>
    )
}