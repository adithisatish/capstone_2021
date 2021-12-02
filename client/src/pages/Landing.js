import React from "react"
import Layout from "../components/layout/Layout"

const Landing = () => {
    return (
        <Layout page="landing">
            <div className="flex-col mt-6">
                <div>
                    <p className="text-7xl font-bold text-green-800 text-center ph:text-5xl">
                        Capstone
                    </p>
                </div>
                <div className="w-full lg:mt-12 ph:mb-12">
                    <div className="flex w-5/6 mx-auto items-center ph:flex-col-reverse">
                        <div className="bg-green-200 w-1/2 rounded-2xl p-4 ph:w-full">
                            <p className="text-center font-bold text-green-800 text-xl">About Us</p>
                            <p className="p-2 text-justify text-green-600">
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. 
                                Curabitur sodales ligula in libero. Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. 
                                Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi a tellus consequat imperdiet. Vestibulum sapien. Proin quam. Etiam ultrices. Suspendisse in justo eu magna luctus suscipit. </p>
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