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
  protocolData?: any;
  pendingApproval?: boolean;
}

interface ProtocolChatPanelProps {
  onDocumentUpdate: (content: string, data: any) => void;
}

export function ProtocolChatPanel({ onDocumentUpdate }: ProtocolChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Cześć! Jestem asystentem do tworzenia protokołu przetargu. Pomogę Ci wypełnić wszystkie wymagane sekcje. Od czego chcesz zacząć?",
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

    // Symulacja odpowiedzi asystenta (w przyszłości można podłączyć do backendu)
    setTimeout(() => {
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: getAssistantResponse(userMsg.content),
        time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages(prev => [...prev, botMsg]);
      setIsLoading(false);
    }, 1000);
  };

  const getAssistantResponse = (userMessage: string): string => {
    const lowerMsg = userMessage.toLowerCase();
    
    if (lowerMsg.includes("numer") || lowerMsg.includes("postępowania")) {
      return "Podaj numer postępowania w formacie np. ZP.271.X.2024, gdzie X to kolejny numer zamówienia w danym roku.";
    }
    if (lowerMsg.includes("ofert") || lowerMsg.includes("wykonawc")) {
      return "Ile ofert zostało złożonych w tym postępowaniu? Podaj nazwy wykonawców i ceny ich ofert.";
    }
    if (lowerMsg.includes("termin")) {
      return "Podaj terminy postępowania:\n- Termin składania ofert\n- Termin otwarcia ofert\n- Termin związania ofertą";
    }
    if (lowerMsg.includes("kryteri")) {
      return "Jakie kryteria oceny ofert zastosowano? Standardowo są to:\n- Cena (60%)\n- Inne kryteria (40%)\n\nPodaj szczegóły dotyczące kryteriów i ich wag.";
    }
    if (lowerMsg.includes("wybran") || lowerMsg.includes("najkorzyst")) {
      return "Która oferta została wybrana jako najkorzystniejsza? Podaj:\n- Nazwę wykonawcy\n- Cenę oferty\n- Uzasadnienie wyboru";
    }
    
    return "Rozumiem. Możesz podać mi więcej szczegółów dotyczących:\n- Numeru postępowania\n- Złożonych ofert\n- Terminów\n- Kryteriów oceny\n- Wybranej oferty\n\nW czym konkretnie mogę pomóc?";
  };

  return (
    <aside className="w-96 border-l border-border bg-card flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-border px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-400 animate-pulse' : 'bg-success'}`} />
          <span className="font-medium text-sm text-foreground">Asystent Protokołu</span>
        </div>
        <Button variant="ghost" size="icon-sm" onClick={() => setMessages([{
          id: "1",
          role: "assistant",
          content: "Cześć! Jestem asystentem do tworzenia protokołu przetargu. Pomogę Ci wypełnić wszystkie wymagane sekcje. Od czego chcesz zacząć?",
          time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
        }])}>
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
