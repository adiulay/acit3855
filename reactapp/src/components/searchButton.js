import React from 'react';
import styled from 'styled-components';

function SearchButton() {

    const Title = styled.h1`
        font-size: 1.5em;
        text-align: center;
        color: palevioletred;
    `;

    // Create a <Wrapper> react component that renders a <section> with
    // some padding and a papayawhip background
    const Wrapper = styled.section`
        background: papayawhip;
    `;

    return (
        <Wrapper>
            <Title>Hello World</Title>
        </Wrapper>
    )
}

export default SearchButton;