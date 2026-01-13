import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Index from "../pages/Index";
import { BrowserRouter } from "react-router-dom";

// Mocking some dependencies that might cause issues in a test environment
vi.mock("@/components/ui/button", () => ({
    Button: ({ children, onClick, disabled }: any) => (
        <button onClick={onClick} disabled={disabled}>{children}</button>
    ),
}));

describe("Index Page", () => {
    it("renders the dashboard title", () => {
        render(
            <BrowserRouter>
                <Index />
            </BrowserRouter>
        );
        expect(screen.getByText(/Vigilance Monitor/i)).toBeInTheDocument();
    });

    it("renders the Scan Now button", () => {
        render(
            <BrowserRouter>
                <Index />
            </BrowserRouter>
        );
        expect(screen.getByText(/Scan Now/i)).toBeInTheDocument();
    });
});
