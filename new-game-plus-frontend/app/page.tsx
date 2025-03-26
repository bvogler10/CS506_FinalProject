'use client'

import DemoAPI from "@/api/DemoAPI";
import { useEffect, useState } from "react";

export default function Home() {
  // This is a state variable that will hold the demo text once fetched. It is initially set to null.
  const [demoText, setDemoText] = useState<string | null>(null);

  // This is the useEffect hook which will run once the component is mounted
  // useEffect is very commonly used in React components to run side effects (like fetching data) after the component is mounted
  // You can update the dependency array (the blank "[]" on line 30) to run the effect whenever a variable within the array changes
  useEffect(() => {
    // This is an async function that fetches the demo text from the backend.
    const getDemoText = async () => {
      // Try catch block for error handling
      try {
        // This is the actual fetch request. We are using the DemoAPI class to make the request.
        const fetchedDemoText = await DemoAPI.demoGetRequest();
        // Once the request is successful, we set the demoText state variable to the fetched demo text
        setDemoText(fetchedDemoText);
      } catch (error) {
        // If there is an error, we log the error to the console. In the real app, it would be good to display an error message to the user.
        console.error(error);
      }
    };

    // Call the actual function to fetch the demo text
    void getDemoText();
  }, []);

  // This is the content that will be displayed on the page. It will display the demo text once it is fetched.
  return (
    <div>
      <h1>New Game Plus</h1>
      <h2>{demoText ? demoText : "Loading demo text"}</h2>
    </div>
  );
}
