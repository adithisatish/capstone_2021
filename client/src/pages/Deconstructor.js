import React from "react"
import { Dialog, DialogContent, Button, DialogTitle, DialogActions } from "@material-ui/core"
import Layout from "../components/layout/Layout"
import { levels, metaphors, metaphorLevel } from "../data"
import { showAlert } from '../utils/alert'
import { decServer } from "../utils/axios"
import OutputSelector from "../utils/display_results"
import EllipsisLoader from "../components/layout/EllipsisLoader"
// import OutputSelector from "../utils/display_results"

const Deconstructor = () => {
    const [currentLevel, setCurrentLevel] = React.useState(0)
    const [currentAttribute, setCurrentAttribute] = React.useState(0)
    const [isAggregateOpen, setAggregateOpen] = React.useState(false)
    const [isIndividualOpen, setIndividualOpen] = React.useState(false)
    const [curAttrExplanation, setCurAttrExplanation] = React.useState(0)
    const [isMetaphorOpen, setMetaphorOpen] = React.useState(false)
    const [currentMetaphor, setCurrentMetaphor] = React.useState(metaphors[0].type)
    const [isMetaphorDropdownOpen, setMetaphorDropdown] = React.useState(false)
    const [isLevelDropdownOpen, setLevelDropdown] = React.useState(false)
    const [inputText, setInputText] = React.useState('')
    const [outputJSX, setOutputJSX] = React.useState(null)
    const [isLoading, setIsLoading] = React.useState(false)
   
    const handleAnalysis = () => {
        if(isMetaphorDropdownOpen) setMetaphorDropdown(false);
        if(isMetaphorOpen) setMetaphorOpen(false);        
        
        const component = levels[currentLevel].attributes[currentAttribute].name
        const body = {
            component,
            text: inputText
        }
        setOutputJSX(null)
        setIsLoading(true)
        decServer.post("http://127.0.0.1:5000/deconstructor",body)
        .then(res => {
            setIsLoading(false)
            setOutputJSX(OutputSelector(res.data,component))
            console.log(res)
        })
        .catch(err => {
            setIsLoading(false)
            showAlert("Internal Server Error!","error")
            console.log(err)
        })
    }
    
    const handleSubmit = () => {
        if (metaphorLevel[0] == currentLevel && metaphorLevel[1] === currentAttribute){
            setMetaphorOpen(true)
            return
        }
        handleAnalysis()
    }

    const handleChangeLevel = (level) => {
        setCurrentAttribute(0)
        setCurrentLevel(level)
    }

    const metaphorDropdown = (
        <div className="relative">
            <button 
                className="relative z-10 block p-2 bg-white rounded-md dark:bg-gray-800 focus:outline-none flex shadow-md w-32"
                onClick={(e) => {e.stopPropagation(); setMetaphorDropdown(!isMetaphorDropdownOpen)}}
            >
                <p className='flex-grow text-left'>
                    {currentMetaphor}
                </p>
                <svg class="-mr-1 ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
                
            </button>   
         
            {isMetaphorDropdownOpen ? (<div class="absolute right-0 z-20 mt-2 overflow-hidden bg-white rounded-md shadow-md w-80 dark:bg-gray-800 z-5">
                <div>
                    {metaphors.map(metaphor => (
                        <div                         
                            className={`flex flex-col px-4 py-3 -mx-2 transition-colors duration-200 transform border-b cursor-pointer ${currentMetaphor === metaphor.type ? 'bg-green-600 text-white hover:bg-green-500': 'hover:bg-gray-100 '}`}
                            onClick={() => setCurrentMetaphor(metaphor.type)}
                        >                        
                            <p className="mx-2 text-sm font-bold">
                                {metaphor.type}       
                            </p>
                        </div>
                    ))}
                </div>
            </div>): null}
        </div>
    )


    return (
        <Layout page="deconstructor">
            <div className="w-full">
                <div className="mx-auto w-4/5 mt-3">
                    <div className="flex">
                        <div className="flex-col">
                            <div className="px-2 py-1 text-xl">
                                Level
                            </div>
                            {/* Level dropdown */}
                            <div class="relative inline-block text-left">
                                <div>
                                    <button 
                                        type="button" 
                                        className="inline-flex justify-center w-full rounded-md shadow-sm px-4 py-2 text-sm font-medium text-white focus:outline-none bg-green-800"
                                        onClick={() => setLevelDropdown(!isLevelDropdownOpen)}
                                    >
                                        {levels[currentLevel].level}
                                        <svg class="-mr-1 ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="white" aria-hidden="true">
                                            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                                        </svg>
                                    </button>
                                </div>
                                {isLevelDropdownOpen ? (
                                    <div class="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50" role="menu">
                                        <div class="py-1" role="none">
                                            {levels.map(level => (
                                                <div 
                                                    className="text-gray-700 block px-4 py-2 text-sm cursor-pointer hover:text-gray-500" 
                                                    key={level.key}
                                                    onClick={() => {handleChangeLevel(level.key); setLevelDropdown(false);}}
                                                >{level.level}</div>
                                            ))}
                                        </div>
                                    </div>
                                ): null}
                            </div>
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
                                onChange={e => setInputText(e.target.value)}
                                value={inputText}
                            >
                            </textarea>
                        </div>
                        <div className="w-1/2 h-96 border-l border-green-800 rounded-br-xl bg-green-100 p-4 overflow-y-auto">
                            {isLoading?<EllipsisLoader/>:outputJSX}
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
                        
            {isMetaphorOpen ? (
                <div class="fixed z-10 inset-0 overflow-y-auto shadow-xl" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div 
                            className="fixed inset-0 transition-opacity" aria-hidden="true"
                            style={{backgroundColor: 'rgba(0, 0, 0, 0.5)'}}
                            onClick={() => setMetaphorDropdown(false)}
                        ></div>
                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                        <div 
                            class="inline-block align-bottom bg-white rounded-lg text-left shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
                            onClick={() => setMetaphorDropdown(false)}
                        >
                            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 rounded">
                                <div class="sm:flex sm:items-start">                        
                                    <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                        <h3 class="text-lg leading-6 text-gray-900 mb-4" id="modal-title">
                                            Choose Metaphor Type
                                        </h3>
                                        {metaphors.map(metaphor => (
                                            <p className='text-base'><span className='font-bold'>{metaphor.type}</span>: {metaphor.description}</p>
                                        ))}
                                        <div class="mt-4">
                                            {metaphorDropdown}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded">
                                <button 
                                    type="button" 
                                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-small text-blue-800 sm:ml-3 sm:w-auto sm:text-sm"
                                    onClick={() => handleAnalysis()}
                                >   
                                    SUBMIT
                                </button>
                                <button 
                                    type="button" 
                                    class="mt-3 w-full inline-flex justify-center rounded-md px-4 py-2 text-base font-small text-blue-800 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                                    onClick={() => {setMetaphorOpen(false); setMetaphorDropdown(false)}}
                                >
                                    CANCEL
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            ): null}            

        </Layout>
    )
}

export default Deconstructor