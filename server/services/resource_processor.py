def process_festividades_madrid(content: str) -> list[dict]:
    festivities = []
    lines = content.split('\\n')
    current_festivity = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "INFORMACIÓN SOBRE LOS DÍAS IMPORTANTES Y FESTIVIDADES DE MADRID" in line:
            continue
        if "Nota de información: entrenamiento IA" in line:
            continue
        if "Página" in line:
            continue

        if line.startswith("•"):
            if current_festivity:
                festivities.append(current_festivity)
            current_festivity = {"name": line.replace("•", "").strip(), "description": []}
        elif current_festivity:
            current_festivity["description"].append(line)
        else:
            # This handles the initial text before the first bullet point
            if "Navidad" in line or "El carnaval" in line or "Semana Santa" in line or "Mayo: un mes muy madrileño" in line or "Celebraciones del Orgullo Gay" in line or "Verbenas de verano" in line or "Fiesta Nacional de España" in line or "Fiesta de Todos los Santos" in line or "Virgen de la Almudena" in line or "El puente de diciembre" in line:
                if current_festivity:
                    festivities.append(current_festivity)
                current_festivity = {"name": line.strip(), "description": []}
            elif current_festivity:
                current_festivity["description"].append(line)

    if current_festivity:
        festivities.append(current_festivity)

    # Post-processing to combine description lines and clean up
    for festivity in festivities:
        festivity["description"] = " ".join(festivity["description"]).strip()
        # Clean up extra spaces and newlines within the description
        festivity["description"] = ' '.join(festivity["description"].split())

    return festivities


def process_links_interes(content: str) -> dict:
    links_data = {}
    lines = content.split('\\n')
    current_category = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Asunto:") or line.startswith("Fecha:") or line.startswith("Página"):
            continue

        if line.endswith(":"):
            current_category = line[:-1].strip()
            links_data[current_category] = []
        elif current_category and line.startswith("https://"):
            links_data[current_category].append(line)
        elif current_category and line: # Handle multi-line URLs
            if links_data[current_category] and not links_data[current_category][-1].startswith("https://"):
                links_data[current_category][-1] += line
            elif links_data[current_category]:
                links_data[current_category][-1] += line
    return links_data


def process_madrid_destino(content: str) -> dict:
    madrid_destino_data = {
        "definition": "",
        "main_activities": [],
        "featured_services": [],
        "contact_info": {}
    }
    lines = content.split('\\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Nota de información:") or line.startswith("Página"):
            continue

        if "MADRID DESTINO" in line:
            continue
        elif "1. Definición:" in line:
            current_section = "definition"
        elif "2. Principales actividades:" in line:
            current_section = "main_activities"
        elif "3. Servicios destacados:" in line:
            current_section = "featured_services"
        elif "4. contacto general:" in line:
            current_section = "contact_info"
        elif current_section:
            if current_section == "definition":
                if not madrid_destino_data["definition"]:
                    madrid_destino_data["definition"] = line
                else:
                    madrid_destino_data["definition"] += " " + line
            elif current_section == "main_activities" and line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6."):
                madrid_destino_data["main_activities"].append(line.split('.', 1)[1].strip())
            elif current_section == "featured_services" and line.startswith("●"):
                madrid_destino_data["featured_services"].append(line.replace("●", "").strip())
            elif current_section == "contact_info":
                if "Teléfono:" in line:
                    madrid_destino_data["contact_info"]["phone"] = line.split(":", 1)[1].strip()
                elif "E-mail:" in line:
                    if "registro@madrid-destino.com" in line:
                        madrid_destino_data["contact_info"]["general_email"] = line.split(":", 1)[1].strip()
                    elif "eventos@madrid-destino.com" in line:
                        madrid_destino_data["contact_info"]["events_email"] = line.split(":", 1)[1].strip()
                    elif "turismo@esmadrid.com" in line:
                        madrid_destino_data["contact_info"]["tourism_email"] = line.split(":", 1)[1].strip()
                elif line:
                    if "address" not in madrid_destino_data["contact_info"]:
                        madrid_destino_data["contact_info"]["address"] = line
                    else:
                        madrid_destino_data["contact_info"]["address"] += " " + line

    # Clean up definition
    madrid_destino_data["definition"] = ' '.join(madrid_destino_data["definition"].split())

    return madrid_destino_data


def process_transporte_publico_madrid(content: str) -> dict:
    transport_data = {
        "introduction": "",
        "basic_info_public_transport": {},
        "modalities": []
    }
    lines = content.split('\\n')
    current_section = None
    current_modality = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Nota de información:") or line.startswith("Página"):
            continue

        if "1.Introducción general a la red de transporte de Madrid" in line:
            current_section = "introduction"
            continue
        elif "2. Información básica para utilizar el transporte público de Madrid" in line:
            current_section = "basic_info_public_transport"
            continue
        elif "3. Modalidades de transporte público:" in line:
            current_section = "modalities"
            continue
        elif "4. Transporte privado" in line:
            current_section = "private_transport"
            continue

        if current_section == "introduction":
            transport_data["introduction"] += line + " "
        elif current_section == "basic_info_public_transport":
            if "El billete sencillo" in line:
                transport_data["basic_info_public_transport"]["single_ticket"] = line.replace("•", "").strip()
            elif "El metrobús" in line:
                transport_data["basic_info_public_transport"]["metrobus"] = line.replace("•", "").strip()
            elif "El abono transporte" in line:
                transport_data["basic_info_public_transport"]["transport_pass"] = line.replace("•", "").strip()
            elif "Madrid City Card" in line:
                transport_data["basic_info_public_transport"]["madrid_city_card"] = line.replace("•", "").strip()
            elif "https://tarjetatransportepublico.crtm.es/" in line:
                transport_data["basic_info_public_transport"]["public_transport_card_link"] = line
            else:
                if "description" not in transport_data["basic_info_public_transport"]:
                    transport_data["basic_info_public_transport"]["description"] = ""
                transport_data["basic_info_public_transport"]["description"] += line + " "
        elif current_section == "modalities":
            if line.startswith("3.1. Metro de Madrid:"):
                current_modality = {"name": "Metro de Madrid", "description": "", "links": []}
                transport_data["modalities"].append(current_modality)
            elif line.startswith("3.2. Metro Ligero:"):
                current_modality = {"name": "Metro Ligero", "description": "", "links": []}
                transport_data["modalities"].append(current_modality)
            elif line.startswith("3.3. Cercanías de Madrid:"):
                current_modality = {"name": "Cercanías de Madrid", "description": "", "links": []}
                transport_data["modalities"].append(current_modality)
            elif line.startswith("3.4. Autobuses:"):
                current_modality = {"name": "Autobuses", "description": "", "links": []}
                transport_data["modalities"].append(current_modality)
            elif line.startswith("3.5. Bicicletas:"):
                current_modality = {"name": "Bicicletas", "description": "", "links": []}
                transport_data["modalities"].append(current_modality)
            elif current_modality:
                if line.startswith("https://"):
                    current_modality["links"].append(line)
                else:
                    current_modality["description"] += line + " "
        elif current_section == "private_transport":
            if "4.1. Taxi" in line:
                if "private_transport" not in transport_data:
                    transport_data["private_transport"] = {}
                transport_data["private_transport"]["taxi"] = {"description": ""}
            elif "taxi" in transport_data.get("private_transport", {}):
                transport_data["private_transport"]["taxi"]["description"] += line + " "

    # Clean up descriptions
    transport_data["introduction"] = ' '.join(transport_data["introduction"].split())
    if "description" in transport_data["basic_info_public_transport"]:
        transport_data["basic_info_public_transport"]["description"] = ' '.join(transport_data["basic_info_public_transport"]["description"].split())
    for modality in transport_data["modalities"]:
        modality["description"] = ' '.join(modality["description"].split())
    if "private_transport" in transport_data and "taxi" in transport_data["private_transport"]:
        transport_data["private_transport"]["taxi"]["description"] = ' '.join(transport_data["private_transport"]["taxi"]["description"].split())

    return transport_data