import { Header } from "@/components/Header";
import { ParametersPanel } from "@/components/ParametersPanel";
import { DocumentEditor } from "@/components/DocumentEditor";
import { ChatPanel } from "@/components/ChatPanel";
import { useState, useEffect } from "react";

const Index = () => {
  const [documentContent, setDocumentContent] = useState<string>("");
  const [swzData, setSwzData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Pobierz początkowy szablon przy starcie
  useEffect(() => {
    const fetchInitialTemplate = async () => {
      try {
        const response = await fetch("http://localhost:8000/initial-template");
        if (response.ok) {
          const data = await response.json();
          setDocumentContent(data.markdown_content);
          setSwzData(data.swz_data);
        }
      } catch (error) {
        console.error("Nie udało się pobrać szablonu:", error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchInitialTemplate();
  }, []);

  const handleDocumentUpdate = (newContent: string, newData: any) => {
    // Zastąp całą treść dokumentu nowym markdown (generowanym na bieżąco)
    setDocumentContent(newContent);
    // Merge new data
    setSwzData((prev: any) => ({ ...prev, ...newData }));
  };

  const handleContentChange = (newContent: string) => {
    setDocumentContent(newContent);
  };

  const handleFormChange = (markdownContent: string, newSwzData: any) => {
    setDocumentContent(markdownContent);
    setSwzData(newSwzData);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <ParametersPanel data={swzData} onFormChange={handleFormChange} />
        <DocumentEditor 
          content={documentContent} 
          onContentChange={handleContentChange}
          isLoading={isLoading}
        />
        <ChatPanel onDocumentUpdate={handleDocumentUpdate} />
      </div>
    </div>
  );
};

export default Index;
