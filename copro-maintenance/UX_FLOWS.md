# UX_FLOWS.md — CoproMaintenance

## Product Summary
- **Product**: CoproMaintenance — SaaS gestion maintenance copropriétés
- **Target user**: Syndic professionnel ou bénévole
- **Core job**: Suivre les obligations réglementaires de maintenance des équipements
- **Primary metric**: Nombre d'équipements conformes / total

## Flow: Inscription et premier login
- **User goal**: Créer un compte et accéder au dashboard
- **Entry**: Landing page → "Essai gratuit" button
- **Steps**:
  1. Remplir formulaire (nom, email, mot de passe, société optionnelle)
  2. Submit → POST /api/auth/register
  3. Token stocké dans localStorage + cookie
  4. Redirection vers /dashboard
- **Inputs**: full_name, email, password, confirmPassword, company_name (optional)
- **System behavior**: Valide email unique, hash password, crée user, génère JWT
- **Success state**: Dashboard avec message "Bienvenue ! Commencez par ajouter un immeuble."
- **Error states**:
  - Email déjà utilisé: "Un compte avec cet email existe déjà."
  - Mot de passe < 8 car: "Le mot de passe doit contenir au moins 8 caractères."
  - Champs requis manquants: validation message
- **Empty/loading**: Spinner dans le bouton submit
- **Data persisted**: User in SQLite, JWT in localStorage + cookie

## Flow: Connexion
- **User goal**: Accéder à son espace
- **Entry**: Landing → "Se connecter"
- **Steps**:
  1. Remplir email + mot de passe
  2. Submit → POST /api/auth/login
  3. Token stocké dans localStorage + cookie
  4. Redirection vers /dashboard
- **Error states**:
  - 401: "Email ou mot de passe incorrect."
  - 422: "Données invalides."
- **Success**: Dashboard with stats

## Flow: Ajouter un immeuble
- **User goal**: Enregistrer une copropriété
- **Entry**: Dashboard → "Immeubles" → "Ajouter un immeuble"
- **Steps**:
  1. Formulaire : nom, adresse, ville, code postal, nombre de lots
  2. Submit → POST /api/buildings
  3. Retour à la liste des immeubles
- **Inputs**: name, address, city, postal_code, nb_lots
- **System**: Crée building lié à l'utilisateur connecté
- **Success**: Nouvel immeuble visible dans la liste
- **Error**: Alert inline avec message d'erreur
- **Empty state (no buildings)**: "Aucun immeuble. Ajoutez votre première copropriété."

## Flow: Ajouter un équipement
- **User goal**: Ajouter un équipement à suivre
- **Entry**: Immeuble → "Ajouter un équipement"
- **Steps**:
  1. Sélectionner immeuble (pré-rempli si depuis l'immeuble)
  2. Remplir nom, type (ascenseur/chaudière/extincteur/porte/gaz/électricité/autre)
  3. Optionnel: numéro de série, date d'installation
  4. Submit → POST /api/equipment
  5. Retour à la fiche immeuble
- **Validation**: immeuble requis, nom requis, type requis

## Flow: Ajouter un contrôle maintenance
- **User goal**: Enregistrer un contrôle effectué
- **Entry**: Équipement → "Ajouter un contrôle"
- **Steps**:
  1. Modal: date contrôle, prochaine date, prestataire, statut (OK/Problème), notes
  2. Submit → POST /api/maintenance
  3. Dashboard mis à jour
- **Fields**: equipment_id, control_date, next_control_date, provider_name, status, notes

## Flow: Consulter le dashboard
- **User goal**: Voir l'état de conformité global
- **Entry**: Header → "Dashboard"
- **Content**:
  - Stats cards: total immeubles, équipements, conformes, en retard
  - Upcoming controls (30 jours): liste avec compte à rebours
- **Empty**: "Aucune donnée — commencez par ajouter un immeuble"
- **Loading**: Spinner
- **Error**: "Impossible de charger les données" + retry

## Flow: Voir le calendrier
- **User goal**: Visualiser les contrôles à venir
- **Entry**: Sidebar → "Calendrier"
- **Content**: Contrôles groupés par semaine, avec immeuble, équipement, date
- **Empty**: "Aucun contrôle prévu dans les 30 jours"

## Flow: Télécharger un document
- **User goal**: Ouvrir un rapport de contrôle
- **Entry**: Documents → clic sur document
- **Steps**: Click → fetch GET /api/documents/{id} avec Bearer token → ouvre le fichier
- **Note**: Le token est passé via header Authorization, PAS dans l'URL

## Non-Functional UX
- **Mobile**: Dashboard responsive, sidebar devient sheet/drawer
- **Slow network**: Loading states on every page, disabled buttons during API calls
- **Invalid input**: Inline validation errors
- **Empty account**: Empty states with clear CTAs on every page

## Feature Truth Rule
Every visible feature in the UI must be one of:
- fully working,
- intentionally disabled with clear copy,
- removed from the UI.
