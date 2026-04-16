import "./globals.css";

export const metadata = {
  title: "Auric Task Portal",
  description: "Daily task management for Auric Jewels",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
