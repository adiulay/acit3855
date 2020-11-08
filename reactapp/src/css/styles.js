import styled from 'styled-components';

export const AppContainer = styled.div`
    display: grid;
    // border-style: solid;
`;

export const Title = styled.h1`
    text-align: center;
`;

export const Time = styled.h3`
    text-align: center;
`;

export const Content = styled.div`
    border-radius: 10px;
    background-color: #f2f2f2;
    padding: 20px;
    border-style: solid;
    margin: 5px;
`;

export const ChildContainer = styled.div`
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(304px, 1fr));
    // border-style: solid;
    padding: 20px;
`;

export const Border = styled.div`
    // border-style: solid;
`;