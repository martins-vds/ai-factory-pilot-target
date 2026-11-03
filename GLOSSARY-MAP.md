# Glossary Map

## Contexts

- [Handling](./src/cargotracker/handling/GLOSSARY.md): records what physically happened to cargo (received, loaded, unloaded, customs, claimed)
- Cargo (`src/cargotracker/cargo/`): bookings, itineraries and each cargo's delivery progress; no glossary yet
- Voyage (`src/cargotracker/voyage/`): carrier voyages and their schedules; no glossary yet
- Location (`src/cargotracker/location/`): the locations cargo moves between; no glossary yet

## Relationships

- **Handling → Cargo**: a registered handling event triggers an inspection that re-derives the cargo's delivery progress from its full handling history
- **Handling → Voyage, Location**: a handling event names the location where it happened and, for loads and unloads, the voyage
