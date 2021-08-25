import React from 'react';
import ReactMarkdown from 'react-markdown';

const getMarkdown = (markdown) => {
    return <ReactMarkdown linkTarget="_blank">{markdown}</ReactMarkdown>;
}

export default getMarkdown;