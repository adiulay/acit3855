import React from 'react';
import { useEffect, useState } from 'react';

function Stats() {
    const [stats, setStats] = useState([]);
    const [error, setError] = useState(true);

    const fetchStats = async () => {
        try {
            var grabStats = await fetch('http://ec2-52-24-255-57.us-west-2.compute.amazonaws.com:8100/stats');
        
            var response = await grabStats.json();

            console.log('GET STATS: ', response);
    
            setStats(response)
            setError(false)
        } catch (e) {
            console.log('ERROR fetchStats:', e.message)
            setError(true)
        } finally {
            return
        }
    };

    useEffect(() => {
        setInterval(() => {
            fetchStats();
        }, 2000);
    }, []);

    const statsTemplate = (
        <div>
            <h2>Current Stats</h2>
            <div>
                <p>Domestic Bag Count: {stats.num_domestic_baggages}</p>
                <p>International Bag Count: {stats.num_international_baggages}</p>
                <p>Total Bags: {stats.total_baggages}</p>
                <p>Last updated: {stats.last_updated}</p>
            </div>
        </div>
    );

    const errorTemplate = (
        <div>
            <h2>Current Stats</h2>
            <div>
                <p>Receiving Server is Offline</p>
            </div>
        </div>
    );

    return error === true ? errorTemplate : statsTemplate;
}

export default Stats;