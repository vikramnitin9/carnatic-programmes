#!/usr/bin/env python3
"""
Parse programme markdown files and generate search_data.json
for client-side search on the Jekyll site.

Usage: python3 _scripts/build_search_data.py
"""

import json
import re
from pathlib import Path

DITTO_MARKERS = {'"', "'", 'do', 'ditto', '\u201c', '\u201d', '\u2033', "''"}


def parse_front_matter(text):
    """Extract YAML front matter and return (metadata, body)."""
    if not text.startswith('---'):
        return {}, text
    end = text.index('---', 3)
    fm = text[3:end].strip()
    body = text[end + 3:].strip()
    metadata = {}
    for line in fm.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata, body


def extract_performers(lines):
    """Extract performer names and instruments from bold-formatted lines."""
    performers = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('|') or line.startswith('---'):
            continue

        # **Name** [*alias* **Name2**] — Instrument
        m = re.match(
            r'^\*\*(.+?)\*\*'
            r'(?:\s*\*alias\*\s*\*\*(.+?)\*\*)?'
            r'\s*[—–\-]\s*(.+)$',
            line
        )
        if m:
            name = m.group(1).strip()
            if m.group(2):
                name += ' alias ' + m.group(2).strip()
            performers.append({'name': name, 'role': m.group(3).strip()})
            continue

        # **Name** (standalone, no instrument)
        m2 = re.match(r'^\*\*(.+?)\*\*\s*$', line)
        if m2:
            performers.append({'name': m2.group(1).strip(), 'role': ''})

    return performers


def parse_table(lines):
    """Parse markdown table rows into list of dicts with normalized keys."""
    table_lines = [l.strip() for l in lines if l.strip().startswith('|')]
    if len(table_lines) < 2:
        return []

    # Parse header row
    raw_headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]

    # Normalize header names
    key_map = {
        'song': 'song', 'item': 'song', 'kriti': 'song', 'piece': 'song',
        'raga': 'raga', 'ragam': 'raga', 'raag': 'raga',
        'tala': 'tala', 'talam': 'tala', 'thalam': 'tala',
        'composer': 'composer', 'vaggeyakara': 'composer',
        'performers': 'performers', 'performer': 'performers',
    }
    headers = [key_map.get(h.lower(), h.lower()) for h in raw_headers]

    # Parse data rows, resolving ditto marks
    rows = []
    last_vals = {h: '' for h in headers}

    for line in table_lines[1:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        # Skip separator row
        if all(re.match(r'^[-:]+$', c) for c in cells if c):
            continue

        row = {}
        for i, h in enumerate(headers):
            val = cells[i].strip() if i < len(cells) else ''
            if val.lower() in DITTO_MARKERS:
                val = last_vals.get(h, '')
            else:
                last_vals[h] = val
            row[h] = val

        rows.append(row)

    return rows


def parse_programme(filepath):
    """Parse a programme markdown file into structured data."""
    content = filepath.read_text(encoding='utf-8')
    metadata, body = parse_front_matter(content)

    sections = re.split(r'^## ', body, flags=re.MULTILINE)

    sessions = []
    for section in sections[1:]:
        lines = section.split('\n')
        date = lines[0].strip()
        rest = lines[1:]

        performers = extract_performers(rest)
        songs = parse_table(rest)

        # Normalize song dicts to always have standard keys
        normalized_songs = []
        for s in songs:
            normalized_songs.append({
                'song': s.get('song', ''),
                'raga': s.get('raga', ''),
                'tala': s.get('tala', ''),
                'composer': s.get('composer', ''),
            })

        if performers or normalized_songs:
            sessions.append({
                'date': date,
                'performers': performers,
                'songs': normalized_songs,
            })

    return {
        'year': int(metadata.get('year', 0)),
        'title': metadata.get('title', ''),
        'conference': metadata.get('conference', ''),
        'file': filepath.stem + '.html',
        'sessions': sessions,
    }


def main():
    base_dir = Path(__file__).resolve().parent.parent
    prog_dir = base_dir / 'programmes'
    output = base_dir / 'search_data.json'

    programmes = []
    for f in sorted(prog_dir.glob('*_programmes.md')):
        prog = parse_programme(f)
        programmes.append(prog)
        print(f'  ✓ {f.name}: {len(prog["sessions"])} sessions')

    with open(output, 'w', encoding='utf-8') as fh:
        json.dump(programmes, fh, indent=2, ensure_ascii=False)

    total_sessions = sum(len(p['sessions']) for p in programmes)
    total_songs = sum(len(s['songs']) for p in programmes
                      for s in p['sessions'])
    artists = {perf['name']
               for p in programmes for s in p['sessions']
               for perf in s['performers']}

    print(f'\n✓ Generated {output.name}')
    print(f'  {len(programmes)} programmes, {total_sessions} sessions, '
          f'{total_songs} songs, {len(artists)} unique artists')


if __name__ == '__main__':
    main()
