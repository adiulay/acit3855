// import logo from './logo.svg';
// import './App.css';
import Stats from './components/Stats';
import SearchIndex from './components/SearchIndex';
import RandomBaggageInfo from './components/RandomBaggageInfo';
import {
  AppContainer,
  ChildContainer,
  // Border,
  Title,
  Time,
  Content
} from './css/styles';

import React, {useState, useEffect} from 'react';

function App() {
  const [date, setDate] = useState(new Date().toString())

  function clock() {
    setDate(new Date().toString());
  };

  useEffect(() => {
    setInterval(clock, 1000);
  })

  return (
    <AppContainer>
      <header className="App-header">
        <Title>🛫Baggage DashBoard💼</Title>
        <Time>{date}</Time>
        <ChildContainer>
          <Content>
            <Stats />
          </Content>
          
          <Content>
            <SearchIndex />
          </Content>
          
          <Content>
            <RandomBaggageInfo />
          </Content>
        </ChildContainer>
      </header>
    </AppContainer>
  );
}

export default App;
