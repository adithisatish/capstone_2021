import React from "react"
import getMarkdown from "./markdown"

const Alliteration = ({obj}) => {
    
    // for each sentence
    //     display sentence 
    //     for each alliteration 
    //         display joined
    //         display explanation

    const res = obj.map((sentence, index) => {
        return (
            <div>
                <p className="text-lg">{index+1}. {sentence.sentence}</p>
                <div className="ml-6">
                {
                    sentence.alliteration.length?
                    <React.Fragment>
                        <p className="text-green-800 text-lg">Alliterations: </p>
                        {
                            sentence.alliteration.map((allit, index) => {
                                return (
                                        <React.Fragment>
                                            <p className="font-bold">{index+1}. {allit.joined.split("-").join(" ")}</p>
                                            <p>{getMarkdown(allit.explanation)}</p>
                                            <br></br>
                                        </React.Fragment>
                                )
                            })}
                    </React.Fragment>:
                    <p className="font-bold text-lg">No Alliterations Found!</p>
                }
                </div>
            </div>
        )
    })
    
    if(res.length){
        return <React.Fragment>{res}</React.Fragment>
    }

    return <p className="font-bold text-lg">No Alliterations Found!</p>
}

const SPO = ({obj}) => {
    // for each sentence
    //     display sentence
    //     for each triple 
    //         display subj + expl
    //         display verb + expl
    //         for each obj_clause
    //             display obj_c + expl (same index number)
    //         for each argm
    //             display argm
    const [page, setPage] = React.useState(0)

    console.log(obj)

    const changePage = (delta) => {
        setPage(Math.max(0, Math.min(page+delta, obj.length-1))) //max(0, min(page+delta, length))
    }

    const res = (
        <div className="text-justify">
            <div className="flex items-center">
                <div className="flex-grow"></div>
                <div className="flex items-center w-40 ">
                    <div className="cursor-pointer flex flex-grow items-end flex-col" onClick={() => changePage(-1)}>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-chevron-left" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <polyline points="15 6 9 12 15 18" />
                        </svg>
                    </div>
                    <div>
                        <p className="text-center">{page+1}/{obj.length}</p>
                    </div>
                    <div className="flex-grow cursor-pointer" onClick={() => changePage(1)}>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-chevron-right" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <polyline points="9 6 15 12 9 18" />
                        </svg>
                    </div>
                </div>
            </div>
            <p className="text-lg">{page+1}. {obj[page].sentence}</p>
            <div className="ml-6">
            {
                obj[page].triplets.length?
                <React.Fragment>
                    <p className="text-green-800 text-lg mb-2">SPO Extractions: </p>
                    {
                        obj[page].triplets.map((spo, index) => {
                            return (
                                <div>
                                    <p className="font-bold mb-1">{index + 1}. Subject: {spo.Subject}</p>
                                    <p>{getMarkdown(spo["Subject Explanation"])}</p>
                                    <p className="font-bold mt-1 mb-1">Verb: {spo["Connecting Verb"]}</p>
                                    <p>{getMarkdown(spo['Verb Explanation'])}</p>

                                    <div>
                                        {
                                            spo['Object Clauses'].length?
                                            <React.Fragment>
                                            <p className="font-bold mt-1 mb-1">Object Clauses: </p>
                                            {
                                                spo['Object Clauses'].map((obj_clause,index) => {
                                                    return (
                                                        <div className="ml-4">
                                                            <p className="font-bold italic">{index+1}. Object: {obj_clause}</p>
                                                            <p>{getMarkdown(spo['Object Explanations'][index])}</p>
                                                        </div>
                                                    )
                                                })
                                            }
                                            </React.Fragment>:null
                                        }
                                    </div>

                                    <div>
                                    {
                                        Object.keys(spo['Argument Modifiers']).length?
                                        <React.Fragment>
                                            <p className="font-bold ml-1 mb-1">Argument Modifiers: </p>
                                                {
                                                    Object.keys(spo['Argument Modifiers']).map(arg_mod => {
                                                        return (
                                                            <div className="ml-4">
                                                                <p><b>{arg_mod}</b>: {spo['Argument Modifiers'][arg_mod]}</p>
                                                            </div>
                                                        )
                                                    })
                                                }
                                        </React.Fragment>:null
                                    }
                                    </div>
                                    <br></br>
                                </div>                                    
                            )                                
                        })
                    }
                </React.Fragment>:
                <p>No subjects, predicates or objects found!</p>
            }
            </div>
        </div>
    )

    return res

}

const Tense = ({obj}) => {
    
    // for each sentence
    //     display sentence 
    //     for each alliteration 
    //         display joined
    //         display explanation

    const res = obj.map((sentence, index) => {
        return (
            <div>
                <p className="text-lg">{index+1}. {sentence.sentence}</p>
                <div className="ml-6">
                    <p className="font-bold">Tense: {sentence.tense}</p>
                    <p className="italic">{getMarkdown(sentence.explanation)}</p>
                    <br></br>
                </div>
            </div>
        )
    })
    
    if(res.length){
        return <React.Fragment>{res}</React.Fragment>
    }

    return <p className="font-bold text-lg">No Tense Found!</p>
}

const Simile = ({obj}) => {
    
    // for each sentence
    //     display sentence 
    //     for each alliteration 
    //         display joined
    //         display explanation
    console.log(obj)
    const res = obj.map((sentence, index) => {
        return (
            <div>
                <p className="text-lg">{index+1}. {sentence.Sentence}</p>
                <div className="ml-6">
                {
                    sentence.Simile.length?
                    <React.Fragment>
                        <p className="text-green-800 text-lg">Similes: </p>
                        {
                                sentence.Simile.map((simile, index) => {
                                return (
                                        <React.Fragment>
                                            <p className="font-bold">{index+1}. {simile}</p>
                                            <p>{getMarkdown(simile.Explanation)}</p>
                                            
                                        </React.Fragment>
                                )
                            })}{                      
                            sentence.Explanation.map((exp, index) => {
                                return (
                                        <React.Fragment>
                                            <p className="italic">{getMarkdown(exp)}</p>
                                            <br></br>
                                        </React.Fragment>
                                )
                            })
                        }
                    </React.Fragment>:
                    <p className="font-bold text-lg">No Similes Found!</p>
                }
                </div>
            </div>
        )
    })
    
    if(res.length){
        return <React.Fragment>{res}</React.Fragment>
    }

    return <p className="font-bold text-lg">No Similes Found!</p>
}

const Voice = ({obj}) => {
    
    // for each sentence
    //     display sentence 
    //     for each alliteration 
    //         display joined
    //         display explanation

    const res = obj.map((sentence, index) => {
        return (
            <div>
                <p className="text-lg">{index+1}. {sentence.sentence}</p>
                <div className="ml-6">
                    <p className="font-bold">Voice: {sentence.voice}</p>
                    <p className="italic">{getMarkdown(sentence.explanation)}</p>
                    <br></br>
                </div>
            </div>
        )
    })
    
    if(res.length){
        return <React.Fragment>{res}</React.Fragment>
    }

    return <p className="font-bold text-lg">No Voice Found!</p>
}

const RhymeScheme = ({obj}) => {
    
    // for each sentence
    //     display sentence 
    //     for each alliteration 
    //         display joined
    //         display explanation

    const schemeSentence = obj.map(sentence => sentence.Letter).join(", ")
    
    
    const res = obj.map((sentence, index) => {
        return (
            <div>
                <p className="text-lg">{index+1}. {sentence.Line}</p>
                <div className="ml-6">
                    <p className="font-bold">Scheme: {sentence.Letter}</p>
                    <p className="italic">Rhyming Word: {sentence.Word}</p>
                    <br></br>
                </div>
            </div>
        )
    })
    
    if(res.length){
        return <React.Fragment>
            <p className="text-xl font-bold mb-2">Rhyme Scheme: {schemeSentence}</p>
            {res}</React.Fragment>
    }

    return <p className="font-bold text-lg">No Rhyme Scheme Found!</p>
}

const Metaphor = ({obj}) => {
// Sentence:
// Potential Noun Metaphors 
// 1. <word1> and <word2>: exp
// Potential Verb Metaphors
// Potential Adjective Metaphors
    const [page, setPage] = React.useState(0)

    // console.log(obj)

    const changePage = (delta) => {
        setPage(Math.max(0, Math.min(page+delta, obj.length-1))) //max(0, min(page+delta, length))
    }

    const res = (
            <React.Fragment>
                <div>
                    <div className="flex items-center">
                        <div className="flex-grow"></div>
                        <div className="flex items-center w-40 ">
                            <div className="cursor-pointer flex flex-grow items-end flex-col" onClick={() => changePage(-1)}>
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-chevron-left" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <polyline points="15 6 9 12 15 18" />
                                </svg>
                            </div>
                            <div>
                                <p className="text-center">{page+1}/{obj.length}</p>
                            </div>
                            <div className="flex-grow cursor-pointer" onClick={() => changePage(1)}>
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-chevron-right" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#2c3e50" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <polyline points="9 6 15 12 9 18" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    <p className="text-lg">{page+1}. {obj[page].sentence}</p>

                    <p className="text-md font-bold mt-2">Possible Adjective Metaphors:</p>
                    {obj[page].adj_metaphors.map((metaphor_maybe, index) => {
                        if(["Y", "N"].includes(metaphor_maybe.result[1])){
                            return <p className="ml-4">{index+1}. {metaphor_maybe.result[0].join(" and ")}: <span className="italic">{getMarkdown(metaphor_maybe.explanation)}</span></p>
                        }
                        return <p className = "italic ml-4">{getMarkdown(metaphor_maybe.explanation)}</p>
                    })}

                    <p className="text-md font-bold mt-2">Possible Noun Metaphors:</p>
                    {obj[page].noun_metaphors.map((metaphor_maybe, index) => {
                        if(["Y", "N"].includes(metaphor_maybe.result[1])){
                            return <p className="ml-4">{index+1}. {metaphor_maybe.result[0].join(" and ")}: <span className="italic">{getMarkdown(metaphor_maybe.explanation)}</span></p>
                        }
                        return <p className = "italic ml-4">{getMarkdown(metaphor_maybe.explanation)}</p>
                    })}

                    <p className="text-md font-bold mt-2">Possible Verb Metaphors:</p>
                    {obj[page].verb_metaphors.map((metaphor_maybe, index) => {
                        if(["Y", "N"].includes(metaphor_maybe.result[1])){
                            return <p className="ml-4">{index+1}. {metaphor_maybe.result[0].join(" and ")}: <span className="italic">{getMarkdown(metaphor_maybe.explanation)}</span></p>
                        }
                        return <p className = "italic ml-4">{getMarkdown(metaphor_maybe.explanation)}</p>
                    })}
                </div>
            </React.Fragment>
        )

return res

}


const OutputSelector = (obj, type) => {
    // const display_result = {Alliteration, SPO}
    console.log(type)
    switch(type){
        case "SPO":
            return <SPO obj={obj}></SPO>
        case "Alliteration":
            return <Alliteration obj = {obj}></Alliteration>
        case "Tense":
            return <Tense obj = {obj}></Tense>
        case "Similes":
            return <Simile obj = {obj}></Simile>
        case "Voice":
            return <Voice obj = {obj}></Voice>
        case "Rhyme Scheme":
            return <RhymeScheme obj = {obj}></RhymeScheme>
        case "Metaphor":
            return <Metaphor obj = {obj}></Metaphor>
        default:
            return null
    }
}


export default OutputSelector