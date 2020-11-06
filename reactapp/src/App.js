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
  Content
} from './css/styles';

function App() {
  return (
    <AppContainer>
      <header className="App-header">
        <Title>Baggage Handling</Title>
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
