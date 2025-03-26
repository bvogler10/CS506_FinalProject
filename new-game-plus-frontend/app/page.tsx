'use client'

import DemoAPI from "@/api/DemoAPI";
import { useEffect, useState } from "react";

export default function Home() {
  const [demoText, setDemoText] = useState<string | null>(null);

  useEffect(() => {
    const getDemoText = async () => {
      try {
        const fetchedDemoText = await DemoAPI.demoGetRequest();
        setDemoText(fetchedDemoText);
      } catch (error) {
        console.error(error);
      }
    };

    void getDemoText();
  }, []);

  return (
    <div>
      <h1>New Game Plus</h1>
      <h2>{demoText ? demoText : "Loading demo text"}</h2>
    </div>
  );
}
