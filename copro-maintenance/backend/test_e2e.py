import httpx
import asyncio

BASE = "http://localhost:8900/api"


async def main():
    async with httpx.AsyncClient() as c:
        # 1. Register
        print("=== REGISTER ===")
        r = await c.post(
            f"{BASE}/auth/register",
            json={
                "email": "syndic@test.fr",
                "password": "secret123",
                "full_name": "Jean Dupont",
                "company": "SyndicPro",
            },
        )
        assert r.status_code == 201, f"Register failed: {r.status_code} {r.text}"
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"OK - token: {token[:20]}...")

        # 2. Login
        print("\n=== LOGIN ===")
        r = await c.post(
            f"{BASE}/auth/login",
            json={"email": "syndic@test.fr", "password": "secret123"},
        )
        assert r.status_code == 200, f"Login failed: {r.status_code}"
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("OK")

        # 3. Get me
        print("\n=== GET ME ===")
        r = await c.get(f"{BASE}/auth/me", headers=headers)
        assert r.status_code == 200
        assert r.json()["email"] == "syndic@test.fr"
        print(f"OK - {r.json()['full_name']}")

        # 4. Create building
        print("\n=== CREATE BUILDING ===")
        r = await c.post(
            f"{BASE}/buildings",
            headers=headers,
            json={
                "name": "Residence Les Oliviers",
                "address": "15 rue de la Paix",
                "city": "Paris",
                "postal_code": "75001",
                "nb_lots": 24,
            },
        )
        assert r.status_code == 201
        bid = r.json()["id"]
        print(f"OK - id={bid}")

        # 5. List buildings
        print("\n=== LIST BUILDINGS ===")
        r = await c.get(f"{BASE}/buildings", headers=headers)
        assert r.status_code == 200
        assert len(r.json()) == 1
        print(f"OK - {len(r.json())} building(s)")

        # 6. Get building detail
        print("\n=== GET BUILDING ===")
        r = await c.get(f"{BASE}/buildings/{bid}", headers=headers)
        assert r.status_code == 200
        print(f"OK - {r.json()['name']}")

        # 7. Update building
        print("\n=== UPDATE BUILDING ===")
        r = await c.put(
            f"{BASE}/buildings/{bid}",
            headers=headers,
            json={"nb_lots": 30},
        )
        assert r.status_code == 200
        assert r.json()["nb_lots"] == 30
        print(f"OK - lots={r.json()['nb_lots']}")

        # 8. Create equipment
        print("\n=== CREATE EQUIPMENT ===")
        r = await c.post(
            f"{BASE}/equipment",
            headers=headers,
            json={
                "building_id": bid,
                "name": "Ascenseur principal",
                "equipment_type": "ascenseur",
                "serial_number": "ASC-2024-001",
                "next_control_date": "2026-09-15",
            },
        )
        assert r.status_code == 201
        eid = r.json()["id"]
        print(f"OK - id={eid}, type={r.json()['equipment_type']}")

        # Create second equipment with overdue status
        r2 = await c.post(
            f"{BASE}/equipment",
            headers=headers,
            json={
                "building_id": bid,
                "name": "Chaudiere gaz",
                "equipment_type": "chaudiere",
                "status": "overdue",
            },
        )
        assert r2.status_code == 201

        # 9. List equipment
        print("\n=== LIST EQUIPMENT ===")
        r = await c.get(f"{BASE}/equipment", headers=headers)
        assert r.status_code == 200
        assert len(r.json()) == 2
        print(f"OK - {len(r.json())} equipment")

        # 10. Filter equipment by building
        print("\n=== FILTER EQUIPMENT ===")
        r = await c.get(f"{BASE}/equipment", params={"building_id": bid}, headers=headers)
        assert r.status_code == 200
        assert len(r.json()) == 2
        print(f"OK - filtered to {len(r.json())}")

        # 11. Get equipment detail
        print("\n=== GET EQUIPMENT ===")
        r = await c.get(f"{BASE}/equipment/{eid}", headers=headers)
        assert r.status_code == 200
        assert r.json()["name"] == "Ascenseur principal"
        print("OK")

        # 12. Update equipment
        print("\n=== UPDATE EQUIPMENT ===")
        r = await c.put(
            f"{BASE}/equipment/{eid}",
            headers=headers,
            json={"status": "pending"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "pending"
        print(f"OK - status={r.json()['status']}")

        # 13. Add maintenance record
        print("\n=== ADD MAINTENANCE ===")
        r = await c.post(
            f"{BASE}/maintenance",
            headers=headers,
            json={
                "equipment_id": eid,
                "control_date": "2026-05-01",
                "next_control_date": "2026-11-01",
                "provider_name": "Otis",
                "provider_phone": "01 23 45 67 89",
                "result": "ok",
                "notes": "Controle semestriel OK",
            },
        )
        assert r.status_code == 201
        print(f"OK - id={r.json()['id']}")

        # 14. Get equipment records
        print("\n=== GET RECORDS ===")
        r = await c.get(f"{BASE}/equipment/{eid}/records", headers=headers)
        assert r.status_code == 200
        assert len(r.json()) == 1
        print(f"OK - {len(r.json())} record(s)")

        # 15. Dashboard
        print("\n=== DASHBOARD ===")
        r = await c.get(f"{BASE}/dashboard/summary", headers=headers)
        assert r.status_code == 200
        s = r.json()
        print(
            f"OK - Buildings:{s['total_buildings']} Equip:{s['total_equipment']} "
            f"OK:{s['equipment_ok']} Pending:{s['equipment_pending']} "
            f"Overdue:{s['equipment_overdue']} Upcoming:{len(s['upcoming_controls'])}"
        )

        # 16. Upload document
        print("\n=== UPLOAD DOCUMENT ===")
        r = await c.post(
            f"{BASE}/documents/upload",
            params={"equipment_id": eid},
            headers={"Authorization": headers["Authorization"]},
            files={"file": ("rapport.pdf", b"fake pdf content", "application/pdf")},
        )
        assert r.status_code == 201
        doc_id = r.json()["id"]
        print(f"OK - doc_id={doc_id}")

        # 17. List and download documents
        print("\n=== DOCUMENTS ===")
        r = await c.get(f"{BASE}/documents", headers=headers)
        assert r.status_code == 200
        assert len(r.json()) == 1
        r2 = await c.get(f"{BASE}/documents/{doc_id}", headers=headers)
        assert r2.status_code == 200
        assert r2.content == b"fake pdf content"
        print(f"OK - list:{len(r.json())}, download:{len(r2.content)} bytes")

        # 18. Delete equipment
        print("\n=== DELETE EQUIPMENT ===")
        r = await c.delete(f"{BASE}/equipment/{eid}", headers=headers)
        assert r.status_code == 204
        print("OK")

        # 19. Delete building
        print("\n=== DELETE BUILDING ===")
        r = await c.delete(f"{BASE}/buildings/{bid}", headers=headers)
        assert r.status_code == 204
        print("OK")

        # 20. Verify cascade
        print("\n=== VERIFY CASCADE ===")
        r = await c.get(f"{BASE}/buildings", headers=headers)
        assert len(r.json()) == 0
        r = await c.get(f"{BASE}/equipment", headers=headers)
        assert len(r.json()) == 0
        print("OK - all cleaned up")

        print("\n=== ALL 20 TESTS PASSED ===")


asyncio.run(main())
