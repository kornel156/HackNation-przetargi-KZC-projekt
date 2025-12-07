import { Header } from "@/components/Header";
import { ParametersPanel } from "@/components/ParametersPanel";
import { DocumentEditor } from "@/components/DocumentEditor";
import { ChatPanel } from "@/components/ChatPanel";
import { useState } from "react";

const Index = () => {
  const [documentContent, setDocumentContent] = useState<string>("");
  const [swzData, setSwzData] = useState<any>(null);

  const handleDocumentUpdate = (newContent: string, newData: any) => {
    // Append new content to existing content
    setDocumentContent((prev) => prev + "\n\n" + newContent);
    // Merge new data
    setSwzData((prev: any) => ({ ...prev, ...newData }));
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <ParametersPanel data={swzData} />
        <DocumentEditor content={documentContent} />
        <ChatPanel onDocumentUpdate={handleDocumentUpdate} />
      </div>
    </div>
  );
};

export default Index;
