import { useState } from "react";
import { Building2, ChevronRight, ChevronDown, Upload, FileText, Calendar, User, MapPin, Clock } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import ComplianceBadge from "./ComplianceBadge";
import ScoreProgress from "./ScoreProgress";

type ComplianceStatus = "compliant" | "clarification" | "non-compliant";

interface OfferDetails {
  description: string;
  submissionDate: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  deliveryTime: string;
  paymentTerms: string;
  technicalRequirements: string[];
  documents: string[];
}

interface Offer {
  id: string;
  companyName: string;
  totalPrice: number;
  evaluationScore: number;
  compliance: ComplianceStatus;
  warranty: number;
  details: OfferDetails;
}

const offers: Offer[] = [
  {
    id: "1",
    companyName: "Budimex S.A.",
    totalPrice: 1240000,
    evaluationScore: 92,
    compliance: "compliant",
    warranty: 60,
    details: {
      description: "Kompleksowa budowa obiektu użyteczności publicznej zgodnie z dokumentacją projektową",
      submissionDate: "2024-01-15",
      contactPerson: "Jan Kowalski",
      email: "jan.kowalski@budimex.pl",
      phone: "+48 22 123 45 67",
      address: "ul. Stawki 40, 01-040 Warszawa",
      deliveryTime: "18 miesięcy",
      paymentTerms: "30 dni od daty wystawienia faktury",
      technicalRequirements: [
        "Certyfikat ISO 9001:2015",
        "Doświadczenie min. 5 lat w budownictwie",
        "Zdolność kredytowa min. 2 mln PLN",
      ],
      documents: ["Oferta_Budimex.pdf", "Referencje.pdf", "Certyfikaty.pdf"],
    },
  },
  {
    id: "2",
    companyName: "Strabag Sp. z o.o.",
    totalPrice: 1350000,
    evaluationScore: 88,
    compliance: "clarification",
    warranty: 48,
    details: {
      description: "Realizacja inwestycji budowlanej z wykorzystaniem nowoczesnych technologii",
      submissionDate: "2024-01-14",
      contactPerson: "Anna Nowak",
      email: "anna.nowak@strabag.com",
      phone: "+48 22 987 65 43",
      address: "ul. Parzniewska 10, 05-800 Pruszków",
      deliveryTime: "20 miesięcy",
      paymentTerms: "45 dni od daty wystawienia faktury",
      technicalRequirements: [
        "Certyfikat ISO 14001",
        "Ubezpieczenie OC min. 5 mln PLN",
        "Kadra inżynierska min. 10 osób",
      ],
      documents: ["Oferta_Strabag.pdf", "Polisa_OC.pdf"],
    },
  },
  {
    id: "3",
    companyName: "Skanska S.A.",
    totalPrice: 1410000,
    evaluationScore: 85,
    compliance: "compliant",
    warranty: 48,
    details: {
      description: "Budowa obiektu z zastosowaniem zrównoważonych materiałów budowlanych",
      submissionDate: "2024-01-13",
      contactPerson: "Piotr Wiśniewski",
      email: "piotr.wisniewski@skanska.pl",
      phone: "+48 22 561 00 00",
      address: "ul. Gen. J. Zajączka 9, 01-518 Warszawa",
      deliveryTime: "16 miesięcy",
      paymentTerms: "21 dni od daty wystawienia faktury",
      technicalRequirements: [
        "Certyfikat LEED",
        "Doświadczenie w projektach zielonych",
        "Własny sprzęt budowlany",
      ],
      documents: ["Oferta_Skanska.pdf", "LEED_Certificate.pdf", "Sprzęt.pdf"],
    },
  },
  {
    id: "4",
    companyName: "Mota-Engil",
    totalPrice: 1190000,
    evaluationScore: 76,
    compliance: "non-compliant",
    warranty: 36,
    details: {
      description: "Realizacja projektu budowlanego w standardzie podstawowym",
      submissionDate: "2024-01-12",
      contactPerson: "Maria Zielińska",
      email: "m.zielinska@mota-engil.pl",
      phone: "+48 71 334 40 00",
      address: "ul. Wadowicka 8W, 30-415 Kraków",
      deliveryTime: "24 miesiące",
      paymentTerms: "60 dni od daty wystawienia faktury",
      technicalRequirements: [
        "Podstawowe certyfikaty budowlane",
        "Doświadczenie min. 3 lata",
      ],
      documents: ["Oferta_MotaEngil.pdf"],
    },
  },
];

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat("pl-PL", {
    style: "decimal",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(price);
};

const getCompanyIconColor = (index: number): string => {
  const colors = [
    "bg-blue-100 text-blue-600",
    "bg-purple-100 text-purple-600",
    "bg-red-100 text-red-600",
    "bg-slate-100 text-slate-600",
  ];
  return colors[index % colors.length];
};

const OffersTable = () => {
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const toggleRow = (id: string) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  return (
    <div className="bg-card rounded-xl border border-border overflow-hidden animate-fade-in">
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent border-border">
            <TableHead className="font-semibold text-foreground">Company Name</TableHead>
            <TableHead className="font-semibold text-foreground">Total Price</TableHead>
            <TableHead className="font-semibold text-foreground">Evaluation Score</TableHead>
            <TableHead className="font-semibold text-foreground">Compliance</TableHead>
            <TableHead className="font-semibold text-foreground">Warranty</TableHead>
            <TableHead className="font-semibold text-foreground text-right">Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {offers.map((offer, index) => (
            <>
              <TableRow
                key={offer.id}
                className="hover:bg-secondary/50 transition-colors border-border cursor-pointer"
                onClick={() => toggleRow(offer.id)}
              >
                <TableCell>
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-9 h-9 rounded-lg flex items-center justify-center ${getCompanyIconColor(index)}`}
                    >
                      <Building2 className="w-4 h-4" />
                    </div>
                    <span className="font-medium text-foreground">{offer.companyName}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <span className="text-foreground">
                    {formatPrice(offer.totalPrice)} PLN
                  </span>
                </TableCell>
                <TableCell>
                  <ScoreProgress score={offer.evaluationScore} />
                </TableCell>
                <TableCell>
                  <ComplianceBadge status={offer.compliance} />
                </TableCell>
                <TableCell>
                  <span className="text-foreground">{offer.warranty} Months</span>
                </TableCell>
                <TableCell className="text-right">
                  <button 
                    className="inline-flex items-center gap-1 text-primary text-sm font-medium hover:underline"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleRow(offer.id);
                    }}
                  >
                    Details
                    {expandedRows.has(offer.id) ? (
                      <ChevronDown className="w-4 h-4" />
                    ) : (
                      <ChevronRight className="w-4 h-4" />
                    )}
                  </button>
                </TableCell>
              </TableRow>

              {/* Expanded Details Row */}
              {expandedRows.has(offer.id) && (
                <TableRow key={`${offer.id}-details`} className="bg-secondary/30 border-border">
                  <TableCell colSpan={6} className="p-0">
                    <div className="p-6 space-y-6 animate-fade-in">
                      {/* Description */}
                      <div>
                        <h4 className="font-semibold text-foreground mb-2">Opis zamówienia</h4>
                        <p className="text-muted-foreground">{offer.details.description}</p>
                      </div>

                      {/* Info Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                            <Calendar className="w-4 h-4 text-primary" />
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground">Data złożenia</p>
                            <p className="text-sm font-medium text-foreground">{offer.details.submissionDate}</p>
                          </div>
                        </div>

                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                            <User className="w-4 h-4 text-primary" />
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground">Osoba kontaktowa</p>
                            <p className="text-sm font-medium text-foreground">{offer.details.contactPerson}</p>
                            <p className="text-xs text-muted-foreground">{offer.details.email}</p>
                          </div>
                        </div>

                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                            <MapPin className="w-4 h-4 text-primary" />
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground">Adres</p>
                            <p className="text-sm font-medium text-foreground">{offer.details.address}</p>
                          </div>
                        </div>

                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                            <Clock className="w-4 h-4 text-primary" />
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground">Czas realizacji</p>
                            <p className="text-sm font-medium text-foreground">{offer.details.deliveryTime}</p>
                          </div>
                        </div>
                      </div>

                      {/* Technical Requirements & Documents */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <h4 className="font-semibold text-foreground mb-3">Wymagania techniczne</h4>
                          <ul className="space-y-2">
                            {offer.details.technicalRequirements.map((req, i) => (
                              <li key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
                                <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                                {req}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <h4 className="font-semibold text-foreground mb-3">Załączone dokumenty</h4>
                          <div className="space-y-2">
                            {offer.details.documents.map((doc, i) => (
                              <div
                                key={i}
                                className="flex items-center gap-2 p-2 bg-card rounded-lg border border-border"
                              >
                                <FileText className="w-4 h-4 text-primary" />
                                <span className="text-sm text-foreground">{doc}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Payment Terms */}
                      <div className="p-4 bg-card rounded-lg border border-border">
                        <p className="text-sm">
                          <span className="font-medium text-foreground">Warunki płatności: </span>
                          <span className="text-muted-foreground">{offer.details.paymentTerms}</span>
                        </p>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center gap-3 pt-2">
                        <Button variant="outline" className="gap-2">
                          <Upload className="w-4 h-4" />
                          Upload SWZ
                        </Button>
                        <Button variant="outline" className="gap-2">
                          <FileText className="w-4 h-4" />
                          Pobierz ofertę
                        </Button>
                      </div>
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default OffersTable;
