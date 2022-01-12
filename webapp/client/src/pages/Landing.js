import React from "react"
import Layout from "../components/layout/Layout"

const Landing = () => {
    return (
        <Layout page="landing">
            <div className="flex-col mt-6">
                <div>
                    <p className="text-7xl font-bold text-green-800 text-center ph:text-5xl">
                        iREAD
                    </p>
                </div>
                <div className="w-full lg:mt-12 ph:mb-12">
                    <div className="flex w-5/6 mx-auto items-center ph:flex-col-reverse">
                        <div className="bg-green-200 w-1/2 rounded-2xl p-4 ph:w-full">
                            <p className="text-center font-bold text-green-800 text-xl">About Us</p>
                            <p className="p-2 text-justify text-green-600">
                                iREAD is a learning aid that uses Machine Learning and Natural Language Processing 
                                techniques to deconstruct passages and identify literary devices and 
                                grammatical rules pertaining to Tense, Tone, Rhyme Schemes, and Metaphors, 
                                amongst others. The techniques used provide an insight to the rationale 
                                behind the deconstruction using: (1) an intuitive explanation through 
                                explication of the rules that underlie the grammatical constructs and 
                                (2) identifying the most relevant features for machine classification 
                                as a way to explain the outcome of models. We validate the algorithms 
                                that underlie the learning aid on manually annotated datasets from high 
                                school textbooks on English Grammar that are widely prescribed and referred 
                                to. The various components are delineated to three learning levels: easy
                                (recognition of subject-predicate-object, tense and tone), intermediate 
                                (recognition of simile, alliteration and rhyme scheme) and advanced 
                                (recognition of metaphor and voice). </p>
                        </div>
                        <div className="p-12 w-1/2 ph:w-full">
                            <img src="./images/girl_reading.svg" className="w-full"/>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    )
}

export default Landing