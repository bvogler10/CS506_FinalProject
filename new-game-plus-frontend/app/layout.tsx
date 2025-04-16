import type { Metadata } from "next";
import "./globals.css";

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
        {children}
      </body>
    </html>
  );
}
