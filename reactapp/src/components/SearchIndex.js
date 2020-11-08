import React from 'react';
import { useEffect, useState } from 'react';

function SearchIndex() {
    const [userInput, setUserInput] = useState('');
    const [index, setIndex] = useState('');
    const [indexInfo, setIndexInfo] = useState([]);
    const [error, setError] = useState({ error: true });

    const fetchBaggageIndex = async (index) => {
        if (index === '') {
            setError({ error: true,  message: '' })
            return
        }

        var convertToNumber = Number(index);

        try {
            var fetchInfoDomestic = await fetch(`http://ec2-52-24-255-57.us-west-2.compute.amazonaws.com:8110/domestic?index=${convertToNumber}`);
            var fetchInfoInternational = await fetch(`http://ec2-52-24-255-57.us-west-2.compute.amazonaws.com:8110/international?index=${convertToNumber}`);

            // var fetchInfoDomestic = await fetch(`https://jsonplaceholder.typicode.com/posts/${convertToNumber}`);
            // var fetchInfoInternational = await fetch(`https://jsonplaceholder.typicode.com/posts/${convertToNumber}`);

            var responseDomestic = await fetchInfoDomestic.json();
            var responseInternational = await fetchInfoInternational.json();

            // console.log('RESPONSE DOMESTIC: ', responseDomestic)
            // console.log('RESPONSE INT: ', responseInternational)

            // var messageTemplate = { message: "Not Found" }
            const domesticTemplate = (
                <div>
                    <h3>Domestic Baggage Info for index: {index}</h3>
                    <p>Baggage ID: {responseDomestic.baggage_id}</p>
                    <p>Weight (kg): {responseDomestic.weight_kg}</p>
                    <p>Destination Province: {responseDomestic.destination_province}</p>
                    <p>Postal Code: {responseDomestic["postal-code"]}</p>
                    <p>Timestamp: {responseDomestic.timestamp}</p>
                </div>
            )

            const internationalTemplate = (
                <div>
                    <h3>International Baggage Info for index: {index}</h3>
                    <p>Baggage ID: {responseInternational.baggage_id}</p>
                    <p>Weight (kg): {responseInternational.weight_kg}</p>
                    <p>Destination: {responseInternational.destination}</p>
                    <p>Timestamp: {responseInternational.timestamp}</p>
                </div>
            )

            var messageTemplate = <p>Not Found</p>

            if ("message" in responseDomestic) {
                responseDomestic = (
                    <div>
                        <h3>Domestic Baggage Info for index: {index}</h3>
                        {messageTemplate}
                    </div>
                )
            } else {
                responseDomestic = domesticTemplate
            }
            
            if ("message" in responseInternational) {
                responseInternational = (
                    <div>
                        <h3>International Baggage Info for index: {index}</h3>
                        {messageTemplate}
                    </div>
                )
            } else {
                responseInternational = internationalTemplate
            }

            setIndexInfo([responseDomestic, responseInternational]);
            setError({ error: false });
        } catch (e) {
            console.log('ERROR fetchBaggageIndex: ', e.message)
            setError({ error: true, message: 'Kafka Server is offline' });
        }
        
    };
    
    useEffect(() => {
        fetchBaggageIndex(index);
    }, [index])

    const handleSubmit = (e) => {
        e.preventDefault();

        // checks input is real number
        var number = Number(userInput);
        if (userInput === '') {
            setError({ error: true, message: 'Value must not be empty' })
            return
        } else if (isNaN(number) === true) {
            setError({ error: true, message: 'Value must be a number' });
            return
        } else {
            setError({ error: false })
            setIndex(userInput);
        }
    }

    const handleChange = (e) => {
        setUserInput(e.target.value);
    }

    
    const indexTemplate = (
        <div>
            <h2>Search by Index</h2>
            <form onSubmit={handleSubmit}>
                <input onChange={handleChange}></input>
                <button type="submit">Search</button>
            </form>
            <div>
                {indexInfo[0]}
            </div>
            <div>
                {indexInfo[1]}
            </div>
        </div>
    )

    const errorTemplate = (
        <div>
            <h2>Search by Index</h2>
            <form onSubmit={handleSubmit}>
                <input onChange={handleChange}></input>
                <button type="submit">Search</button>
            </form>
            <p>{error.message}</p>
        </div>
    )

    return error.error ? errorTemplate : indexTemplate;
}

export default SearchIndex;