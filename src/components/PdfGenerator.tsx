import { Document, Page, Text, View, StyleSheet, Font, pdf } from '@react-pdf/renderer';

// Register Polish-compatible font
Font.register({
  family: 'Roboto',
  fonts: [
    { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-regular-webfont.ttf', fontWeight: 'normal' },
    { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf', fontWeight: 'bold' },
    { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-italic-webfont.ttf', fontStyle: 'italic' },
  ]
});

const styles = StyleSheet.create({
  page: {
    padding: 50,
    fontFamily: 'Roboto',
    fontSize: 11,
    lineHeight: 1.5,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 12,
    textAlign: 'center',
    marginBottom: 5,
  },
  h1: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
    textAlign: 'center',
  },
  h2: {
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 8,
  },
  h3: {
    fontSize: 12,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 6,
  },
  paragraph: {
    marginBottom: 8,
    textAlign: 'justify',
  },
  bold: {
    fontWeight: 'bold',
  },
  italic: {
    fontStyle: 'italic',
  },
  listItem: {
    marginBottom: 4,
    paddingLeft: 15,
  },
  horizontalRule: {
    borderBottomWidth: 1,
    borderBottomColor: '#000',
    marginVertical: 15,
  },
  header: {
    marginBottom: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    paddingBottom: 10,
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 50,
    right: 50,
    textAlign: 'center',
    fontSize: 9,
    color: '#666',
  },
});

interface ParsedElement {
  type: 'h1' | 'h2' | 'h3' | 'paragraph' | 'listItem' | 'hr';
  content: string;
  children?: ParsedElement[];
}

function parseMarkdown(markdown: string): ParsedElement[] {
  const lines = markdown.split('\n');
  const elements: ParsedElement[] = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    if (!line) continue;
    
    if (line.startsWith('### ')) {
      elements.push({ type: 'h3', content: line.slice(4) });
    } else if (line.startsWith('## ')) {
      elements.push({ type: 'h2', content: line.slice(3) });
    } else if (line.startsWith('# ')) {
      elements.push({ type: 'h1', content: line.slice(2) });
    } else if (line === '---' || line === '***') {
      elements.push({ type: 'hr', content: '' });
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      elements.push({ type: 'listItem', content: line.slice(2) });
    } else if (/^\d+\.\s/.test(line)) {
      elements.push({ type: 'listItem', content: line });
    } else {
      elements.push({ type: 'paragraph', content: line });
    }
  }
  
  return elements;
}

function renderTextWithFormatting(text: string) {
  // Handle bold and italic
  const parts: React.ReactNode[] = [];
  let remaining = text;
  let key = 0;
  
  while (remaining.length > 0) {
    // Check for bold **text**
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    // Check for italic *text*
    const italicMatch = remaining.match(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/);
    
    if (boldMatch && boldMatch.index !== undefined) {
      if (boldMatch.index > 0) {
        parts.push(<Text key={key++}>{remaining.slice(0, boldMatch.index)}</Text>);
      }
      parts.push(<Text key={key++} style={styles.bold}>{boldMatch[1]}</Text>);
      remaining = remaining.slice(boldMatch.index + boldMatch[0].length);
    } else if (italicMatch && italicMatch.index !== undefined) {
      if (italicMatch.index > 0) {
        parts.push(<Text key={key++}>{remaining.slice(0, italicMatch.index)}</Text>);
      }
      parts.push(<Text key={key++} style={styles.italic}>{italicMatch[1]}</Text>);
      remaining = remaining.slice(italicMatch.index + italicMatch[0].length);
    } else {
      parts.push(<Text key={key++}>{remaining}</Text>);
      break;
    }
  }
  
  return parts;
}

interface SWZDocumentProps {
  content: string;
}

function SWZDocument({ content }: SWZDocumentProps) {
  const elements = parseMarkdown(content);
  
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        {elements.map((element, index) => {
          switch (element.type) {
            case 'h1':
              return <Text key={index} style={styles.h1}>{renderTextWithFormatting(element.content)}</Text>;
            case 'h2':
              return <Text key={index} style={styles.h2}>{renderTextWithFormatting(element.content)}</Text>;
            case 'h3':
              return <Text key={index} style={styles.h3}>{renderTextWithFormatting(element.content)}</Text>;
            case 'hr':
              return <View key={index} style={styles.horizontalRule} />;
            case 'listItem':
              return (
                <Text key={index} style={styles.listItem}>
                  • {renderTextWithFormatting(element.content)}
                </Text>
              );
            case 'paragraph':
            default:
              return (
                <Text key={index} style={styles.paragraph}>
                  {renderTextWithFormatting(element.content)}
                </Text>
              );
          }
        })}
        <Text style={styles.footer} render={({ pageNumber, totalPages }) => (
          `Strona ${pageNumber} z ${totalPages}`
        )} fixed />
      </Page>
    </Document>
  );
}

export async function generatePdf(markdown: string): Promise<Blob> {
  const blob = await pdf(<SWZDocument content={markdown} />).toBlob();
  return blob;
}

export function downloadPdf(blob: Blob, filename: string = 'dokument-swz.pdf') {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
