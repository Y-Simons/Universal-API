import React from 'react';

export const metadata = {
  title: 'Anesth AI',
  description: "AI-assisted pre/post-op workflows for anesthetists"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body style={{ fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji"', margin: 0 }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: 16 }}>
          <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0' }}>
            <h1 style={{ fontSize: 20, margin: 0 }}>Anesth AI</h1>
            <a href="/dashboard">Tableau de bord</a>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}