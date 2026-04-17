import folium
import geopandas as gpd

# 1. Initialisation de la carte centrée sur le Sénégal
ma_carte = folium.Map(location=[14.4974, -14.4524], zoom_start=7)

# Ajout du fond Satellite Hybride
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google',
    name='Satellite (Google)',
    overlay=False
).add_to(ma_carte)

# 2. Création des groupes (FeatureGroups)
group_dakar    = folium.FeatureGroup(name="Dakar (Région)")
group_route    = folium.FeatureGroup(name="Dakar (Routes)")
group_kaolack  = folium.FeatureGroup(name="Kaolack (Départements)")
group_localite = folium.FeatureGroup(name="Kaolack (Localité)")
group_kedougou = folium.FeatureGroup(name="Kédougou (Région)")
group_occsol   = folium.FeatureGroup(name="Kédougou (Occsol)")

# 3. Fonction pour charger et ajouter proprement à un groupe
def charger_et_ajouter(chemin, groupe, couleur, label):
    try:
        data = gpd.read_file(chemin)
        if data.crs != "EPSG:4326":
            data = data.to_crs(epsg=4326)

        # ✅ Correction du piège lambda : couleur=couleur capture la valeur locale
        folium.GeoJson(
            data,
            name=label,
            style_function=lambda x, c=couleur: {
                'fillColor': c,
                'color': c,
                'weight': 2,
                'fillOpacity': 0.4
            }
        ).add_to(groupe)
        print(f"✅ {label} chargé avec succès.")
    except Exception as e:
        print(f"❌ Erreur sur {chemin}: {e}")

# 4. Chargement des fichiers
charger_et_ajouter("DAKAR_REG.shp",                          group_dakar,    "blue",   "Dakar Région")
charger_et_ajouter("Reseau_Routier_SN.shp",                  group_route,    "black",  "Dakar Routes")
charger_et_ajouter("DPT KAOLACK.shp",                        group_kaolack,  "green",  "Kaolack Départements")
charger_et_ajouter("localite.shp",                   group_localite, "pink",   "Kaolack Localités")
charger_et_ajouter("kedougou.shp",                    group_kedougou, "red",    "Kédougou Région")
charger_et_ajouter("occsol_2020_KEDOUGOU_ND-28-VI.shp",      group_occsol,   "yellow", "Kédougou Occsol")

# 5. ✅ Ajout de TOUS les groupes à la carte
group_dakar.add_to(ma_carte)
group_route.add_to(ma_carte)
group_kaolack.add_to(ma_carte)
group_localite.add_to(ma_carte)
group_kedougou.add_to(ma_carte)
group_occsol.add_to(ma_carte)

# 6. Contrôle des couches
folium.LayerControl(collapsed=False).add_to(ma_carte)

# 7. Sauvegarde
ma_carte.save("Index.html")
print("\nFélicitations ! Ton projet est prêt dans 'Index.html'.")