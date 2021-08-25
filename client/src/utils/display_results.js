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

    const res = obj.map(sentence => {
        return (
            <li>
                <p>{sentence.sentence}</p>
                <ul>
                {
                    sentence.triplets.map(spo => {
                        return (
                            <li>
                                <p>{spo.Subject}</p>
                                <p>{spo["Subject Explanation"]}</p>
                                <p>{spo.Verb}</p>
                                <p>{spo['Verb Explanation']}</p>

                                <ul>
                                    {
                                        spo['Object Clauses'].map((obj_clause,index) => {
                                            return (
                                                <li>
                                                    <p>{obj_clause}</p>
                                                    <p>{spo['Object Explanations'][index]}</p>
                                                </li>
                                            )
                                        })
                                    }
                                </ul>

                                <ul>
                                    {
                                        Object.keys(spo['Argument Modifiers']).map(arg_mod => {
                                            return (
                                                <li>
                                                    <p>{arg_mod}: {spo['Argument Modifiers'][arg_mod]}</p>
                                                </li>
                                            )
                                        })
                                    }
                                </ul>

                            </li>
                        )
                    })
                }
                </ul>
            </li>
        )
        })

        if(res.length){
            return <ol>{res}</ol>
        }

        return <p>No subjects, predicates or objects found!</p>

}

const display_result = {Alliteration, SPO}
export default display_result