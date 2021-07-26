import React from "react"
import { Dialog, DialogContent, Button, DialogTitle, DialogActions } from "@material-ui/core"
import Layout from "../components/layout/Layout"
import { levels, metaphors, metaphorLevel } from "../data"

const Deconstructor = () => {
    const [currentLevel, setCurrentLevel] = React.useState(0)
    const [currentAttribute, setCurrentAttribute] = React.useState(0)
    const [isAggregateOpen, setAggregateOpen] = React.useState(false)
    const [isIndividualOpen, setIndividualOpen] = React.useState(false)
    const [curAttrExplanation, setCurAttrExplanation] = React.useState(0)
    const [isMetaphorOpen, setMetaphorOpen] = React.useState(false)
    const [currentMetaphor, setCurrentMetaphor] = React.useState(metaphors[0].type)

    const handleChangeMetaphor = (metaphor) => {
        setCurrentMetaphor(metaphor)
    }

    const handleAnalysis = () => {
        alert("Hi")
        setMetaphorOpen(false)
    }
    
    const handleSubmit = () => {
        if (metaphorLevel[0] == currentLevel && metaphorLevel[1] === currentAttribute){
            setMetaphorOpen(true)
            return
        }
        console.log(currentLevel, currentAttribute)
        handleAnalysis()
    }

    const handleChangeLevel = (level) => {
        setCurrentAttribute(0)
        setCurrentLevel(level)
    }

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
                        <div className="w-1/2 relative">
                            {/* Submit Button */}
                            <div 
                                className="flex items-center justify-center w-12 h-12 bg-green-800 absolute bottom-4 right-4 rounded-3xl shadow-xl cursor-pointer"
                                onClick={() => handleSubmit()}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-send" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="lightgrey" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                    <line x1="10" y1="14" x2="21" y2="3"></line>
                                    <path d="M21 3l-6.5 18a0.55 .55 0 0 1 -1 0l-3.5 -7l-7 -3.5a0.55 .55 0 0 1 0 -1l18 -6.5"></path>
                                </svg>
                            </div>
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
                    {/* <div className="flex">
                        <div className="w-1/2 flex">
                            <button className="rounded bg-green-800 px-4 py-2 text-white ml-auto mt-2">Deconstruct</button>
                        </div>
                    </div> */}
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

            <Dialog
                open= {isMetaphorOpen}
                onClose= {() => setMetaphorOpen(false)}
            >
                <DialogTitle>Types of Metaphors</DialogTitle>
                <DialogContent>
                    <div className="ml-6">
                        {
                            metaphors.map((metaphor) => <p>
                                <span className="font-bold">
                                    {metaphor.type}
                                </span>: {metaphor.description}
                            </p>)
                        }
                    </div>
                    <div className="flex items-center">
                        <select 
                            className="p-2 rounded border border-green-800 bg-green-800 text-white focus:outline-none cursor-pointer mx-auto mt-4"
                            value={currentMetaphor}
                            onChange={(e) => handleChangeMetaphor(e.target.value)}
                        >
                            {
                                metaphors.map(metaphor => <option value={metaphor.type}>{metaphor.type}</option>)
                            }
                        </select>
                    </div>                
                </DialogContent>
                <DialogActions>
                <Button onClick={() => handleAnalysis()} color="primary">
                    Submit
                </Button>
                <Button onClick={() => setMetaphorOpen(false)} color="primary">
                    Close
                </Button>
                </DialogActions>
            </Dialog>

        </Layout>
    )
}

export default Deconstructor