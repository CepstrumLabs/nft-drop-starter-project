import React, {useState, useEffect } from 'react';
import './CountdownTimer.css';

const CountdownTimer = ({ dropDate }) => {

    const [timerString, setTimerString] = useState('');
    
    return (
        <div className='timer-container'>
            <p className='timer-header'>
                Candy drop starting in
            </p> 
            { timerString && <p className='timer-value'> `⏰ ${timerString}` </p>}
        </div>
    )
};

export default CountdownTimer;
