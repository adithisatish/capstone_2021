import React from "react"
import getMarkdown from "./markdown"

const Alliteration = (obj) => {
    
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
const SPO = (obj) => {
    // for each sentence
    //     display sentence
    //     for each triple 
    //         display subj + expl
    //         display verb + expl
    //         for each obj_clause
    //             display obj_c + expl (same index number)
    //         for each argm
    //             display argm

    const res = obj.map((sentence, index) => {
        return (
            <div className="text-justify">
                <p className="text-lg">{index+1}. {sentence.sentence}</p>
                <div className="ml-6">
                {
                    sentence.triplets.length?
                    <React.Fragment>
                        <p className="text-green-800 text-lg mb-2">SPO Extractions: </p>
                        {
                            sentence.triplets.map((spo, index) => {
                                return (
                                    <div>
                                        <p className="font-bold mb-1">{index + 1}. Subject: {spo.Subject}</p>
                                        <p>{getMarkdown(spo["Subject Explanation"])}</p>
                                        <p className="font-bold mt-1 mb-1">Verb: {spo["Connecting Verb"]}</p>
                                        <p>{getMarkdown(spo['Verb Explanation'])}</p>

                                        <div>
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
                                        </div>

                                        <div>
                                        {
                                            spo['Argument Modifiers'].length?
                                            <React.Fragment>
                                                <p className="font-bold ml-1 mb-1">Argument Modifiers: </p>
                                                    {
                                                        Object.keys(spo['Argument Modifiers']).map(arg_mod => {
                                                            return (
                                                                <div className="ml-4">
                                                                    <p>{arg_mod}: {spo['Argument Modifiers'][arg_mod]}</p>
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
        })

        if(res.length){
            return <React.Fragment>{res}</React.Fragment>
        }

        return <p>No subjects, predicates or objects found!</p>

}

const display_result = {Alliteration, SPO}
export default display_result