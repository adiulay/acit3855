import React from 'react';
import { useEffect, useState } from 'react';

function RandomBaggageInfo() {
    const [error, setError] = useState({ error: true });
    const [randomIndex, setRandomIndex] = useState('');
    const [indexInfo, setIndexInfo] = useState('')

    const fetchRandomBaggageIndex = async (randomIndex) => {
        if (randomIndex === '') {
            setError({ error: true,  message: '' })
            return
        }

        try {
            var travelType = ['domestic', 'international'];
            var randomTravelType = travelType[Math.floor(Math.random() * 2)]

            var fetchRandomIndex = await fetch(`http://ec2-52-24-255-57.us-west-2.compute.amazonaws.com:8110/${randomTravelType}?index=${randomIndex}`);
            // var fetchRandomIndex = await fetch(`https://jsonplaceholder.typicode.com/posts/${randomIndex}`)

            var response = await fetchRandomIndex.json();

            const errorMessageTemplate = {
                error: true,
                message: `${response.message} in index ${randomIndex} for ${randomTravelType}.`
            }

            const domesticTemplate = (
                <div>
                    <h3>Domestic Baggage Info for index: {randomIndex}</h3>
                    <p>Baggage ID: {response.baggage_id}</p>
                    <p>Weight (kg): {response.weight_kg}</p>
                    <p>Destination Province: {response.destination_province}</p>
                    <p>Postal Code: {response["postal-code"]}</p>
                    <p>Timestamp: {response.timestamp}</p>
                </div>
            )

            const internationalTemplate = (
                <div>
                    <h3>International Baggage Info for index: {randomIndex}</h3>
                    <p>Baggage ID: {response.baggage_id}</p>
                    <p>Weight (kg): {response.weight_kg}</p>
                    <p>Destination: {response.destination}</p>
                    <p>Timestamp: {response.timestamp}</p>
                </div>
            )

            //TESTING PURPOSES
            if ("message" in response) {
                setError(errorMessageTemplate);
                // console.log('FETCH TRAVEL TYPE: ', randomTravelType);
                // console.log('RESPONSE fetchRandomBaggageIndex: ', response);
            } else {
                // console.log('FETCH TRAVEL TYPE: ', randomTravelType);
                // console.log('RESPONSE fetchRandomBaggageIndex: ', response);
                if (randomTravelType === 'domestic') {
                    response = domesticTemplate
                } else if (randomTravelType === 'international') {
                    response = internationalTemplate
                }
                setError({ error: false })
                setIndexInfo(response)
            }

        } catch (e) {
            console.log('ERROR fetchRandomBaggageIndex: ', e.message);
            setError({ error: true, message: 'Kafka Server is offline'});
        }
    }

    useEffect(() => {
        fetchRandomBaggageIndex(randomIndex);
    }, [randomIndex])

    const handleChange = (e) => {
        e.preventDefault();
        var randomIndex = Math.floor(Math.random() * 11);
        // console.log('CLICKED handleChange: ', randomIndex);
        setRandomIndex(randomIndex);
    }

    const randomTemplate = (
        <div>
            <h2>Random Baggage Info (0-10)</h2>
            <button onClick={handleChange}>Random</button>
            <div>
              {indexInfo}
            </div>
        </div>
    )
    
    const errorTemplate = (
        <div>
            <h2>Random Baggage Info (0-10)</h2>
            <button onClick={handleChange}>Random</button>
            <div>
              <p>{error.message}</p>
            </div>
        </div>
    )

    return error.error ? errorTemplate : randomTemplate;
}

export default RandomBaggageInfo;