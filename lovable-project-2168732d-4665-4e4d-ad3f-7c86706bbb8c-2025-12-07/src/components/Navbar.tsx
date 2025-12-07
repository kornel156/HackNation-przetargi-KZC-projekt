import { Search, FileText } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

const Navbar = () => {
  const navItems = [
    { label: "Dashboard", active: false },
    { label: "Analiza Ofert", active: true },
    { label: "Reports", active: false },
    { label: "Settings", active: false },
  ];

  return (
    <header className="bg-card border-b border-border px-6 py-3">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-primary" />
            </div>
            <span className="font-semibold text-foreground">E-Reporting Platform</span>
          </div>

          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search tenders..."
              className="pl-10 w-64 bg-secondary border-0 focus-visible:ring-1 focus-visible:ring-primary"
            />
          </div>
        </div>

        <nav className="flex items-center gap-8">
          <ul className="hidden md:flex items-center gap-6">
            {navItems.map((item) => (
              <li key={item.label}>
                <a
                  href="#"
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    item.active ? "text-primary" : "text-muted-foreground"
                  }`}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>

          <Avatar className="w-9 h-9 border-2 border-orange-200">
            <AvatarFallback className="bg-orange-100 text-orange-600 text-sm font-medium">
              U
            </AvatarFallback>
          </Avatar>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
