import { CheckCircle2, AlertCircle, XCircle } from "lucide-react";

type ComplianceStatus = "compliant" | "clarification" | "non-compliant";

interface ComplianceBadgeProps {
  status: ComplianceStatus;
}

const statusConfig = {
  compliant: {
    label: "Compliant",
    icon: CheckCircle2,
    className: "bg-success/10 text-success",
  },
  clarification: {
    label: "Clarification",
    icon: AlertCircle,
    className: "bg-warning/20 text-warning",
  },
  "non-compliant": {
    label: "Non-Compliant",
    icon: XCircle,
    className: "bg-destructive/10 text-destructive",
  },
};

const ComplianceBadge = ({ status }: ComplianceBadgeProps) => {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${config.className}`}
    >
      <Icon className="w-3.5 h-3.5" />
      {config.label}
    </span>
  );
};

export default ComplianceBadge;
