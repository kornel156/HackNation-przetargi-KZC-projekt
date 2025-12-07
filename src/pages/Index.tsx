import { useState } from "react";
import { Header } from "@/components/Header";
import { ParametersPanel } from "@/components/ParametersPanel";
import { DocumentEditor } from "@/components/DocumentEditor";
import { ChatPanel } from "@/components/ChatPanel";

const Index = () => {
  const [documentContent, setDocumentContent] = useState<string | undefined>(undefined);

  const handleDocumentUpdate = (content: string) => {
    setDocumentContent(content);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <ParametersPanel />
        <DocumentEditor content={documentContent} onContentChange={handleDocumentUpdate} />
        <ChatPanel onDocumentUpdate={handleDocumentUpdate} />
      </div>
    </div>
  );
};

export default Index;
