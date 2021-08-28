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

const OutputSelector = (obj, type) => {
    // const display_result = {Alliteration, SPO}
    switch(type){
        case "SPO":
            return <SPO obj={obj}></SPO>
        case "Alliteration":
            return <Alliteration obj = {obj}></Alliteration>
        default:
            return null
    }
}


export default OutputSelector