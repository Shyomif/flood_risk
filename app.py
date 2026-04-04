import streamlit as st
import leafmap.foliumap as leafmap
import branca.colormap as cm

# ... (نفس الروابط السابقة) ...

m = leafmap.Map(center=[35.9, 36.6], zoom=10)
m.add_basemap("Esri.WorldImagery")

try:
    # 1. طبقة الحدود (acc)
    m.add_geojson(url_acc_json, layer_name="حدود ACC", style={'color': 'yellow', 'weight': 3, 'dashArray': '5,5', 'fillOpacity':0})

    # 2. إنشاء تدرج لوني مخصص يشبه الصورة تماماً
    # القيم هنا (0, 0.25, 0.5, 0.75, 1) تعبر عن توزيع الألوان
    step_cmap = cm.StepColormap(
        ['#00FFFF', '#00FF00', '#FFFF00', '#FFA500', '#FF0000'],
        vmin=0, vmax=1, # سيتم مواءمتها مع قيم DN تلقائياً
        caption='درجة الخطورة'
    )

    # 3. إضافة البيانات باستخدام التدرج المخصص
    m.add_data(
        url_flood_json,
        column="DN",
        cmap=step_cmap, # نمرر الكائن الذي أنشأناه هنا
        layer_name="مخاطر الفيضانات",
        scheme="Quantiles",
        k=5,
        fill_opacity=0.7
    )

    m.to_streamlit(height=800)
