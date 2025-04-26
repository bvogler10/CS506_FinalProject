import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/global/navbar";

export const metadata: Metadata = {
  title: "New Game Plus",
  description: "Finding your next favorite game",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
