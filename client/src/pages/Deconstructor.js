import React from "react"
import { Dialog, DialogContent, Button, DialogTitle, DialogActions } from "@material-ui/core"
import Layout from "../components/layout/Layout"

const Deconstructor = () => {
    const [currentLevel, setCurrentLevel] = React.useState(0)
    const [currentAttribute, setCurrentAttribute] = React.useState(0)
    const [isAggregateOpen, setAggregateOpen] = React.useState(false)
    const [isIndividualOpen, setIndividualOpen] = React.useState(false)
    const [curAttrExplanation, setCurAttrExplanation] = React.useState(0)

    const handleChangeLevel = (level) => {
        setCurrentAttribute(0)
        setCurrentLevel(level)
    }
    
    const levels = [{
        level: "Easy",
        key: 0,
        attributes: [{
            name: "SPO",
            explanation: "This is subject-predicate-object detection."
        }, {
            name: "Tense",
            explanation: "Tense detection."
        },{
            name: "Tone",
            explanation: "Tone detection."
        }],
        explanation: "Level easy - 5th and 6th grade"
    }, {
        level: "Intermediate",
        key: 1,
        attributes: [{
            name: "Alliteration",
            explanation: "Alliteration detection."
        }, {
            name: "Rhyme Scheme",
            explanation: "Rhyme Scheme detection."
        },{
            name: "Similes",
            explanation: "Simile detection."
        }],
        explanation: "Level intermediate - 7th and 8th grade"
    }, {
        level: "Advanced",
        key: 2,
        attributes: [{
            name: "Metaphor",
            explanation: "Metaphor detection."
        }, {
            name: "Voice",
            explanation: "Voice detection."
        }],
        explanation: "Level advanced - 9th and 10th grade"
    }]

    return (
        <Layout page="deconstructor">
            <div className="w-full">
                <div className="mx-auto w-4/5 mt-3">
                    <div className="flex">
                        <div className="flex-col">
                            <div className="px-2 py-1 text-xl">
                                Level
                            </div>
                            <select 
                                className="p-2 rounded-xl border border-green-800 bg-green-800 text-white focus:outline-none cursor-pointer"
                                value={currentLevel}
                                onChange={(e) => handleChangeLevel(e.target.value)}
                            >
                                {
                                    levels.map(level => <option value={level.key}>{level.level}</option>)
                                }
                            </select>
                        </div>
                        <div className="flex-grow"></div>
                        <button onClick={() => setAggregateOpen(true)}>
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-help" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                <circle cx="12" cy="12" r="9"></circle>
                                <line x1="12" y1="17" x2="12" y2="17.01"></line>
                                <path d="M12 13.5a1.5 1.5 0 0 1 1 -1.5a2.6 2.6 0 1 0 -3 -4"></path>
                            </svg>
                        </button>
                    </div>
                    <div className="flex">
                        <div className="w-1/2"></div>
                        <div className="w-1/2 flex">
                            {
                                levels[currentLevel].attributes.map((attr, index) => {
                                    let style = "border-white"
                                    if(index > 0) style += " border-l";
                                    if(index < levels[currentLevel].attributes.length - 1) style += " border-r";
                                    if(index === 0) style += " rounded-tl-xl"
                                    if(index === levels[currentLevel].attributes.length - 1) style += " rounded-tr-xl"
                                    return (
                                        <div 
                                            className={`flex items-center justify-center flex-grow ${index==currentAttribute?'bg-green-600':'bg-green-800'} text-white text-center p-3 ${style} cursor-pointer`}
                                            onClick= {() => {setCurrentAttribute(index)}}
                                        >
                                            <p>{attr.name}</p>
                                            <button className="ml-2" onClick={(e) => {
                                                e.stopPropagation()
                                                setCurAttrExplanation(index)
                                                setIndividualOpen(true)
                                            }}>
                                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-help" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                                    <circle cx="12" cy="12" r="9"></circle>
                                                    <line x1="12" y1="17" x2="12" y2="17.01"></line>
                                                    <path d="M12 13.5a1.5 1.5 0 0 1 1 -1.5a2.6 2.6 0 1 0 -3 -4"></path>
                                                </svg>
                                            </button>
                                        </div>
                                    )
                                })
                            }
                            
                        </div>
                    </div>
                    <div className="flex h-96">
                        <div className="w-1/2">
                            <textarea 
                                className="form-textarea w-full h-full p-4 bg-green-100 border-transparent focus:border-green-800 focus:ring-0 rounded-l-xl resize-none text-justify"
                                placeholder='Enter text'
                            >
                            </textarea>
                        </div>
                        <div className="w-1/2 h-96 border-l border-green-800 rounded-br-xl bg-green-100 p-4">
                            Hello!
                        </div>                
                    </div>
                </div>
            </div>
            <Dialog
                fullWidth= {true}
                maxWidth= 'md'
                open= {isAggregateOpen}
                onClose= {() => setAggregateOpen(false)}
            >
                <DialogTitle>Explanation of Levels</DialogTitle>
                <DialogContent>
                   <div>
                        {
                            levels.map((level, index) => (  
                                <div>
                                    <p className="mt-4">
                                        <strong className="text-xl">{index + 1}. {level.level}: </strong>{level.explanation}
                                    </p>
                                    <div className="ml-6">
                                        {
                                            level.attributes.map(attr => (
                                                <div>
                                                    <p className="mt-2">
                                                        <strong>{attr.name}: </strong>{attr.explanation}
                                                    </p>
                                                </div>
                                            ))
                                        }
                                    </div>
                                </div>                
                            )) 
                        }
                   </div>
                </DialogContent>
                <DialogActions>
                <Button onClick={() => setAggregateOpen(false)} color="primary">
                    Close
                </Button>
                </DialogActions>
            </Dialog>

            <Dialog
                fullWidth= {true}
                maxWidth= 'md'
                open= {isIndividualOpen}
                onClose= {() => setIndividualOpen(false)}
            >
                <DialogTitle>Explanation of Component</DialogTitle>
                <DialogContent>
                    <div className="ml-6">
                        {
                            <p className="mt-2">
                                <strong>{levels[currentLevel].attributes[curAttrExplanation].name}: </strong>{levels[currentLevel].attributes[curAttrExplanation].explanation}
                            </p>
                        }
                    </div>                
                </DialogContent>
                <DialogActions>
                <Button onClick={() => setIndividualOpen(false)} color="primary">
                    Close
                </Button>
                </DialogActions>
            </Dialog>

        </Layout>
    )
}

export default Deconstructor