import { useState } from "react";
import { Send, Bot, Trash2, User, Check, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useToast } from "@/components/ui/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
  toRender?: boolean;
  swzData?: any;
  pendingApproval?: boolean;
}

interface ChatPanelProps {
  onDocumentUpdate: (content: string, data: any) => void;
}

export function ChatPanel({ onDocumentUpdate }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Cześć! Jestem Twoim asystentem SWZ. W czym mogę pomóc?",
      time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
    };
    
    setMessages(prev => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.content }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
        toRender: data.to_render,
        swzData: data.swz_data,
        pendingApproval: data.to_render // If it needs rendering, it needs approval
      };

      setMessages(prev => [...prev, botMsg]);
      
      // Automatycznie aktualizuj dokument markdown na bieżąco
      if (data.markdown_content) {
        onDocumentUpdate(data.markdown_content, data.swz_data);
      }

    } catch (error) {
      toast({
        title: "Błąd",
        description: "Nie udało się połączyć z asystentem.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = (msg: Message) => {
    if (msg.toRender && msg.content) {
      onDocumentUpdate(msg.content, msg.swzData);
      
      // Update message to remove pending status
      setMessages(prev => prev.map(m => 
        m.id === msg.id ? { ...m, pendingApproval: false } : m
      ));

      toast({
        title: "Zatwierdzono",
        description: "Sekcja została dodana do dokumentu.",
      });
    }
  };

  const handleReject = (msgId: string) => {
    setMessages(prev => prev.map(m => 
      m.id === msgId ? { ...m, pendingApproval: false } : m
    ));
    toast({
      title: "Odrzucono",
      description: "Możesz poprosić asystenta o poprawki.",
    });
  };

  return (
    <aside className="w-96 border-l border-border bg-card flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-border px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-400 animate-pulse' : 'bg-success'}`} />
          <span className="font-medium text-sm text-foreground">Asystent SWZ</span>
        </div>
        <Button variant="ghost" size="icon-sm" onClick={() => setMessages([])}>
          <Trash2 className="w-4 h-4 text-muted-foreground" />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin">
        {messages.map((message, index) => (
          <div
            key={message.id}
            className={cn(
              "flex gap-3 animate-fade-in",
              message.role === "user" && "flex-row-reverse"
            )}
            style={{ animationDelay: `${index * 50}ms` }}
          >
            {message.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-primary-foreground" />
              </div>
            )}
            
            <div className="flex flex-col gap-2 max-w-[280px]">
              <div
                className={cn(
                  "rounded-2xl px-4 py-2.5",
                  message.role === "user"
                    ? "bg-chat-user text-primary-foreground rounded-br-md"
                    : "bg-chat-assistant text-foreground rounded-bl-md"
                )}
              >
                <p className="text-sm whitespace-pre-wrap leading-relaxed">
                  {message.content}
                </p>
                
                <p className={cn(
                  "text-[10px] mt-1",
                  message.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
                )}>
                  {message.time}
                </p>
              </div>

              {/* Approval UI */}
              {message.role === "assistant" && message.pendingApproval && (
                <div className="flex gap-2 bg-muted/50 p-2 rounded-lg border border-border">
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1 h-8 text-xs gap-1 hover:bg-green-100 hover:text-green-700 hover:border-green-200"
                    onClick={() => handleApprove(message)}
                  >
                    <Check className="w-3 h-3" /> Zatwierdź
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1 h-8 text-xs gap-1 hover:bg-red-100 hover:text-red-700 hover:border-red-200"
                    onClick={() => handleReject(message.id)}
                  >
                    <X className="w-3 h-3" /> Odrzuć
                  </Button>
                </div>
              )}
            </div>
            
            {message.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0">
                <User className="w-4 h-4 text-muted-foreground" />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3">
             <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-primary-foreground" />
              </div>
              <div className="bg-chat-assistant rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border">
        <div className="relative">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Zapytaj asystenta..."
            className="pr-10"
            disabled={isLoading}
          />
          <Button
            variant="ghost"
            size="icon-sm"
            className="absolute right-1 top-1/2 -translate-y-1/2 text-primary hover:text-primary"
            onClick={handleSend}
            disabled={isLoading}
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </aside>
  );
}
