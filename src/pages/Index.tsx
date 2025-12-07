import { Header } from "@/components/Header";
import { ParametersPanel } from "@/components/ParametersPanel";
import { DocumentEditor } from "@/components/DocumentEditor";
import { ChatPanel } from "@/components/ChatPanel";

const Index = () => {
  return (
    <div className="h-screen flex flex-col bg-background">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <ParametersPanel />
        <DocumentEditor />
        <ChatPanel />
      </div>
    </div>
  );
};

export default Index;
