import React from 'react';

function RandomBaggageInfo() {
    return (
        <div>
            <h2>Random Baggage Info</h2>
            <button>Random</button>
            <div>
              {/* this is going to be if else for error issues */}
              <p>Baggage ID: number here</p>
              <p>Destination Province: insert</p>
              <p>Postal Code: insert here</p>
              <p>Weight in Kilograms: number here kg</p>
              <p>Timestamp: "timestsamp"</p>
            </div>
        </div>
    )
}

export default RandomBaggageInfo;