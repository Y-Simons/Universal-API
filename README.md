# Universal API — the screen as a universal interface

**Status: research note, ongoing. No implementation in this repository.**

## Idea

Most business software exposes its data through heterogeneous, often closed or
undocumented interfaces. The one interface every application shares is the
screen: whatever a human can read, a system can in principle read too.

This project explores **screen recording (pixels) as a universal, standardised
input for data capture and processing**, as an alternative to building and
maintaining one connector per application.

## Questions studied

- **Feasibility** — which kinds of screens and data (tables, forms, dashboards,
  documents) can be captured reliably from pixels alone?
- **Benefit / cost** — when does a screen-based pipeline beat a classic API or
  connector integration (build time, maintenance, robustness to UI changes,
  latency, compute cost)?
- **Limits** — accuracy, auditability, security and privacy of capturing what is
  displayed on screen.

## Status

Exploratory work. Notes and prototypes will be added here as the analysis
progresses.
