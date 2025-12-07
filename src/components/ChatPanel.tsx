import { useState } from "react";
import { Send, Bot, Trash2, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
  actions?: { label: string; onClick?: () => void }[];
}

const initialMessages: Message[] = [
  {
    id: "1",
    role: "assistant",
    content: 'Cześć! Widzę, że tworzysz SWZ dla "Budowy hali sportowej". Czy chcesz, abym dodał standardowe zapisy dotyczące klauzuli waloryzacyjnej zgodnie z najnowszymi wytycznymi UZP?',
    time: "10:23",
  },
  {
    id: "2",
    role: "user",
    content: "Tak, proszę. Dodaj też wymóg zatrudnienia na umowę o pracę.",
    time: "10:24",
  },
  {
    id: "3",
    role: "assistant",
    content: 'Zaktualizowałem **Sekcję III** o zapisy dotyczące zatrudnienia (art. 95 Pzp). Zaznaczyłem zmiany na żółto.\n\nCo do waloryzacji, proponuję taki zapis w projekcie umowy:\n\n> "Wynagrodzenie podlega waloryzacji w przypadku zmiany cen materiałów lub kosztów..."',
    time: "10:25",
    actions: [
      { label: "Wstaw do dokumentu" },
      { label: "Edytuj treść" },
    ],
  },
];

const quickActions = [
  "Sprawdź błędy",
  "Skróć opis",
  "Dodaj warunek wiedzy",
];

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (!inputValue.trim()) return;
    
    const newMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      time: new Date().toLocaleTimeString("pl-PL", { hour: "2-digit", minute: "2-digit" }),
    };
    
    setMessages([...messages, newMessage]);
    setInputValue("");
  };

  return (
    <aside className="w-96 border-l border-border bg-card flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-border px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-success rounded-full animate-pulse-soft" />
          <span className="font-medium text-sm text-foreground">Asystent AI</span>
        </div>
        <Button variant="ghost" size="icon-sm">
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
              <p className="text-sm whitespace-pre-wrap leading-relaxed">
                {message.content.split(/(\*\*.*?\*\*)/).map((part, i) => {
                  if (part.startsWith("**") && part.endsWith("**")) {
                    return <strong key={i}>{part.slice(2, -2)}</strong>;
                  }
                  if (part.startsWith("> ")) {
                    return (
                      <span key={i} className="block mt-2 pl-3 border-l-2 border-primary/30 italic text-muted-foreground">
                        {part.slice(2)}
                      </span>
                    );
                  }
                  return part;
                })}
              </p>
              
              {message.actions && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {message.actions.map((action, i) => (
                    <Button
                      key={i}
                      variant="action"
                      size="sm"
                      className="h-7 text-xs"
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
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Zapytaj asystenta..."
            className="pr-10"
          />
          <Button
            variant="ghost"
            size="icon-sm"
            className="absolute right-1 top-1/2 -translate-y-1/2 text-primary hover:text-primary"
            onClick={handleSend}
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-[10px] text-muted-foreground mt-2 text-center">
          AI może generować nieścisłości. Zweryfikuj dokument prawnie.
        </p>
      </div>
    </aside>
  );
}
