'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Test cases for ident_utils.py
'''

def test_ident_utils(ident_utils):
    util = ident_utils()
    
    uuidv4: str = util.generate_secure_id()
    assert len(uuidv4) == 36
    assert uuidv4[14] == '4'
    assert uuidv4[19] in '89ab'
    assert uuidv4.count('-') == 4
    
    uuidv7: str = util.generate_lookup_id()
    assert len(uuidv7) == 36
    assert uuidv7[14] == '7'
    assert uuidv7[19] in '89ab'
    assert uuidv7.count('-') == 4
    
    trace_id: str = util.generate_trace_id()
    assert len(trace_id) == 28
    assert trace_id[14] == '_'
    assert trace_id[15] == 't'
    assert all(n.isdigit() for n in trace_id[:14])
    
    nano_id: str = util.generate_nano_id()
    assert len(nano_id) == 16
    assert nano_id[12:16] in util.signature
    
    assert util.id_type(uuidv4) == 'uuid'
    assert util.id_type(uuidv7) == 'uuid'
    assert util.id_type(trace_id) == 'trace_id'
    assert util.id_type(nano_id) == 'nano_id'
    
    assert util.verify_uuid(uuidv4, 'secure')
    assert util.verify_uuid(uuidv7, 'lookup')
    assert util.verify_trace_id(trace_id)
    assert util.verify_nano_id(nano_id)