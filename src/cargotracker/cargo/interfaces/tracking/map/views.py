from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from cargotracker.cargo.interfaces.tracking.map.coordinates import LOCATION_COORDINATES

STATUS_COLORS = {
    'NOT_ROUTED': 'grey',
    'NOT_RECEIVED': 'gold',
    'IN_PORT': 'green',
    'ONBOARD_CARRIER': 'green',
    'MISDIRECTED': 'red',
    'AT_DESTINATION': 'black',
    'CLAIMED': 'black',
    'UNKNOWN': 'red',
}


@xframe_options_sameorigin
def map_frame(request):
    status_code = request.GET.get('statusCode', 'UNKNOWN')
    locations = {
        role: _location_data(request, role)
        for role in ('origin', 'destination', 'lastKnownLocation')
    }
    markers = [
        {
            'role': role,
            **location,
            'coordinates': list(LOCATION_COORDINATES[location['code']]),
            'color': STATUS_COLORS.get(status_code, 'red')
            if role == 'lastKnownLocation'
            else 'black',
        }
        for role, location in locations.items()
        if location['code'] in LOCATION_COORDINATES
    ]
    return render(
        request,
        'cargo/interfaces/tracking/map/frame.html',
        {'map_data': {'statusCode': status_code, **locations, 'markers': markers}},
    )


def _location_data(request, role):
    code = request.GET.get(f'{role}Code', '')
    return {
        'code': code,
        'name': request.GET.get(f'{role}Name', ''),
    }
