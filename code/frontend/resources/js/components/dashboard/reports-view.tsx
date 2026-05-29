import { useState } from 'react';

import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

type ReportRow = {
    region: string;
    cases: number;
    species: string;
    trend: string;
};

type Report = {
    id: string;
    title: string;
    date: string;
    rows: ReportRow[];
};

const PLACEHOLDER_REPORTS: Report[] = [
    {
        id: 'R-001',
        title: 'Wochenbericht HPAI',
        date: '2026-05-26',
        rows: [
            { region: 'Zürich', cases: 12, species: 'Wildvögel', trend: '↑' },
            { region: 'Bern', cases: 7, species: 'Geflügel', trend: '→' },
            { region: 'Genf', cases: 3, species: 'Wildvögel', trend: '↓' },
            { region: 'Tessin', cases: 5, species: 'Geflügel', trend: '↑' },
        ],
    },
    {
        id: 'R-002',
        title: 'Lagebericht ASP Grenzregion',
        date: '2026-05-19',
        rows: [
            { region: 'Basel-Stadt', cases: 0, species: 'Wildschwein', trend: '→' },
            { region: 'Schaffhausen', cases: 2, species: 'Wildschwein', trend: '↑' },
            { region: 'Thurgau', cases: 1, species: 'Wildschwein', trend: '→' },
        ],
    },
    {
        id: 'R-003',
        title: 'Monatsbericht Mai',
        date: '2026-05-01',
        rows: [
            { region: 'Zürich', cases: 42, species: 'Diverse', trend: '↑' },
            { region: 'Bern', cases: 31, species: 'Diverse', trend: '→' },
            { region: 'Waadt', cases: 18, species: 'Diverse', trend: '↓' },
            { region: 'Wallis', cases: 9, species: 'Diverse', trend: '→' },
            { region: 'St. Gallen', cases: 14, species: 'Diverse', trend: '↑' },
        ],
    },
    {
        id: 'R-004',
        title: 'Sonderbericht Geflügel',
        date: '2026-04-22',
        rows: [
            { region: 'Luzern', cases: 4, species: 'Hühner', trend: '↑' },
            { region: 'Aargau', cases: 6, species: 'Enten', trend: '↑' },
            { region: 'Solothurn', cases: 2, species: 'Hühner', trend: '→' },
        ],
    },
];

export default function ReportsView() {
    const [activeReport, setActiveReport] = useState<Report | null>(null);

    return (
        <>
            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>ID</TableHead>
                            <TableHead>Titel</TableHead>
                            <TableHead>Datum</TableHead>
                            <TableHead className="w-[1%] text-right">Aktion</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {PLACEHOLDER_REPORTS.map((r) => (
                            <TableRow key={r.id}>
                                <TableCell className="font-mono text-xs">{r.id}</TableCell>
                                <TableCell>{r.title}</TableCell>
                                <TableCell>{r.date}</TableCell>
                                <TableCell className="text-right">
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => setActiveReport(r)}
                                    >
                                        Details
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            <Dialog
                open={activeReport !== null}
                onOpenChange={(open) => {
                    if (!open) setActiveReport(null);
                }}
            >
                <DialogContent className="sm:max-w-4xl">
                    {activeReport && (
                        <>
                            <DialogHeader>
                                <DialogTitle className="flex items-center gap-2">
                                    <span className="font-mono text-xs text-muted-foreground">
                                        {activeReport.id}
                                    </span>
                                    <span>{activeReport.title}</span>
                                </DialogTitle>
                                <DialogDescription>
                                    Berichtsdatum: {activeReport.date}
                                </DialogDescription>
                            </DialogHeader>

                            <div className="mt-2 max-h-[70vh] overflow-auto rounded-md border">
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Region</TableHead>
                                            <TableHead className="text-right">Fälle</TableHead>
                                            <TableHead>Spezies</TableHead>
                                            <TableHead className="text-center">Trend</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {activeReport.rows.map((row, idx) => (
                                            <TableRow key={idx}>
                                                <TableCell>{row.region}</TableCell>
                                                <TableCell className="text-right tabular-nums">
                                                    {row.cases}
                                                </TableCell>
                                                <TableCell>{row.species}</TableCell>
                                                <TableCell className="text-center">
                                                    {row.trend}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </div>
                        </>
                    )}
                </DialogContent>
            </Dialog>
        </>
    );
}
