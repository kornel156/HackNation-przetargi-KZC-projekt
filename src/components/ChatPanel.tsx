import { useState, useRef, useEffect } from "react";
import { Send, Bot, Trash2, User, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
  actions?: { label: string; onClick?: () => void }[];
}

interface ChatPanelProps {
  onDocumentUpdate?: (content: string) => void;
}

const API_URL = "http://localhost:8000";

const quickActions = [
  "Sprawdź błędy",
  "Skróć opis",
  "Dodaj warunek wiedzy",
];

export function ChatPanel({ onDocumentUpdate }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Cześć! Jestem asystentem do tworzenia dokumentów SWZ. Powiedz mi, jaki dokument chcesz stworzyć lub zadaj pytanie dotyczące zamówień publicznych.",
      time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
      };

      // Check if there's a document draft - check both direct field and state
      const draft = data.swz_draft || data.state?.swz_draft;
      if (draft && onDocumentUpdate) {
        onDocumentUpdate(draft);
      }

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Przepraszam, wystąpił błąd podczas połączenia z serwerem. Upewnij się, że backend jest uruchomiony na porcie 8000.",
        time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: "welcome",
        role: "assistant",
        content: "Cześć! Jestem asystentem do tworzenia dokumentów SWZ. Powiedz mi, jaki dokument chcesz stworzyć lub zadaj pytanie dotyczące zamówień publicznych.",
        time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
      }
    ]);
  };

  const handleQuickAction = (action: string) => {
    setInputValue(action);
  };

  return (
    <aside className="w-96 border-l border-border bg-card flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-border px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={cn(
            "w-2 h-2 rounded-full",
            isLoading ? "bg-yellow-500 animate-pulse" : "bg-success animate-pulse-soft"
          )} />
          <span className="font-medium text-sm text-foreground">Asystent AI</span>
        </div>
        <Button variant="ghost" size="icon-sm" onClick={handleClearChat}>
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
            
            <div
              className={cn(
                "max-w-[280px] rounded-2xl px-4 py-2.5",
                message.role === "user"
                  ? "bg-chat-user text-primary-foreground rounded-br-md"
                  : "bg-chat-assistant text-foreground rounded-bl-md"
              )}
            >
              <div className="text-sm leading-relaxed prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
              
              {message.actions && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {message.actions.map((action, i) => (
                    <Button
                      key={i}
                      variant="action"
                      size="sm"
                      className="h-7 text-xs"
                      onClick={action.onClick}
                    >
                      {action.label}
                    </Button>
                  ))}
                </div>
              )}
              
              <p className={cn(
                "text-[10px] mt-1",
                message.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
              )}>
                {message.time}
              </p>
            </div>
            
            {message.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0">
                <User className="w-4 h-4 text-muted-foreground" />
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-primary-foreground" />
            </div>
            <div className="bg-chat-assistant rounded-2xl rounded-bl-md px-4 py-3">
              <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 border-t border-border">
        <div className="flex flex-wrap gap-2">
          {quickActions.map((action) => (
            <Button
              key={action}
              variant="outline"
              size="sm"
              className="h-7 text-xs"
              onClick={() => handleQuickAction(action)}
            >
              {action}
            </Button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border">
        <div className="relative">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
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
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
        <p className="text-[10px] text-muted-foreground mt-2 text-center">
          AI może generować nieścisłości. Zweryfikuj dokument prawnie.
        </p>
      </div>
    </aside>
  );
}
