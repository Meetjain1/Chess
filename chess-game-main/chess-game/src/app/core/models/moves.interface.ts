export interface Move { 
    newPosition: string[];
    isKill: boolean;
    castle?: Castle;
    enPassant?: EnPassant;
}

interface Castle { 
    rookStartPosition: string[];
    rookEndPosition: string[];
}

interface EnPassant { 
    killPosition: string[];
}