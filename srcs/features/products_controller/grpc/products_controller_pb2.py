# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: features/products_controller/grpc/products_controller.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;features/products_controller/grpc/products_controller.proto\x12\x1c\x62\x61se_app.products_controller\x1a\x1bgoogle/protobuf/empty.proto\"\'\n\x19\x42\x61seProductDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x18\n\x16\x42\x61seProductListRequest\"]\n\x17\x42\x61seProductListResponse\x12\x42\n\x07results\x18\x01 \x03(\x0b\x32\x31.base_app.products_controller.BaseProductResponse\"o\n\x1f\x42\x61seProductPartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\ncategories\x18\x02 \x03(\t\x12\x1e\n\x16_partial_update_fields\x18\x03 \x03(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"B\n\x12\x42\x61seProductRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\ncategories\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"y\n\x13\x42\x61seProductResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\ncategories\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x1e\n\x11polymorphic_ctype\x18\x04 \x01(\x05H\x00\x88\x01\x01\x42\x14\n\x12_polymorphic_ctype\"(\n\x1a\x42\x61seProductRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"$\n\x16\x43\x61tegoryDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x15\n\x13\x43\x61tegoryListRequest\"W\n\x14\x43\x61tegoryListResponse\x12?\n\x07results\x18\x01 \x03(\x0b\x32..base_app.products_controller.CategoryResponse\"X\n\x1c\x43\x61tegoryPartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1e\n\x16_partial_update_fields\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"+\n\x0f\x43\x61tegoryRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\",\n\x10\x43\x61tegoryResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"%\n\x17\x43\x61tegoryRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\")\n\x1b\x43offeeMachineDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x1a\n\x18\x43offeeMachineListRequest\"a\n\x19\x43offeeMachineListResponse\x12\x44\n\x07results\x18\x01 \x03(\x0b\x32\x33.base_app.products_controller.CoffeeMachineResponse\"\x81\x02\n!CoffeeMachinePartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1e\n\x16_partial_update_fields\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\x05\x12\x0c\n\x04heat\x18\x05 \x01(\x02\x12\x13\n\x0bwater_level\x18\x06 \x01(\x05\x12\x18\n\x10used_water_level\x18\x07 \x01(\x05\x12\x14\n\x0c\x63offee_level\x18\x08 \x01(\x05\x12\x17\n\x0f\x66ilter_position\x18\t \x01(\x08\x12\x12\n\nmode_value\x18\n \x01(\x05\x12\x12\n\ncategories\x18\x0b \x03(\x03\"\xd4\x01\n\x14\x43offeeMachineRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x0c\n\x04heat\x18\x04 \x01(\x02\x12\x13\n\x0bwater_level\x18\x05 \x01(\x05\x12\x18\n\x10used_water_level\x18\x06 \x01(\x05\x12\x14\n\x0c\x63offee_level\x18\x07 \x01(\x05\x12\x17\n\x0f\x66ilter_position\x18\x08 \x01(\x08\x12\x12\n\nmode_value\x18\t \x01(\x05\x12\x12\n\ncategories\x18\n \x03(\x03\"\x8b\x02\n\x15\x43offeeMachineResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x0c\n\x04heat\x18\x04 \x01(\x02\x12\x13\n\x0bwater_level\x18\x05 \x01(\x05\x12\x18\n\x10used_water_level\x18\x06 \x01(\x05\x12\x14\n\x0c\x63offee_level\x18\x07 \x01(\x05\x12\x17\n\x0f\x66ilter_position\x18\x08 \x01(\x08\x12\x12\n\nmode_value\x18\t \x01(\x05\x12\x1e\n\x11polymorphic_ctype\x18\n \x01(\x05H\x00\x88\x01\x01\x12\x12\n\ncategories\x18\x0b \x03(\x03\x42\x14\n\x12_polymorphic_ctype\"*\n\x1c\x43offeeMachineRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"#\n\x15LedModeDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x14\n\x12LedModeListRequest\"U\n\x13LedModeListResponse\x12>\n\x07results\x18\x01 \x03(\x0b\x32-.base_app.products_controller.LedModeResponse\"W\n\x1bLedModePartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1e\n\x16_partial_update_fields\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"*\n\x0eLedModeRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"a\n\x0fLedModeResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1e\n\x11polymorphic_ctype\x18\x03 \x01(\x05H\x00\x88\x01\x01\x42\x14\n\x12_polymorphic_ctype\"$\n\x16LedModeRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"$\n\x16LedPanelDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x15\n\x13LedPanelListRequest\"W\n\x14LedPanelListResponse\x12?\n\x07results\x18\x01 \x03(\x0b\x32..base_app.products_controller.LedPanelResponse\"\xac\x01\n\x1cLedPanelPartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1e\n\x16_partial_update_fields\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\x05\x12\x12\n\nbrightness\x18\x05 \x01(\x01\x12\x11\n\x04mode\x18\x06 \x01(\x03H\x00\x88\x01\x01\x12\x12\n\ncategories\x18\x07 \x03(\x03\x42\x07\n\x05_mode\"\x7f\n\x0fLedPanelRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x12\n\nbrightness\x18\x04 \x01(\x01\x12\x11\n\x04mode\x18\x05 \x01(\x03H\x00\x88\x01\x01\x12\x12\n\ncategories\x18\x06 \x03(\x03\x42\x07\n\x05_mode\"\xb6\x01\n\x10LedPanelResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x12\n\nbrightness\x18\x04 \x01(\x01\x12\x1e\n\x11polymorphic_ctype\x18\x05 \x01(\x05H\x00\x88\x01\x01\x12\x11\n\x04mode\x18\x06 \x01(\x03H\x01\x88\x01\x01\x12\x12\n\ncategories\x18\x07 \x03(\x03\x42\x14\n\x12_polymorphic_ctypeB\x07\n\x05_mode\"%\n\x17LedPanelRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"#\n\x15ProjectDestroyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x14\n\x12ProjectListRequest\"U\n\x13ProjectListResponse\x12>\n\x07results\x18\x01 \x03(\x0b\x32-.base_app.products_controller.ProjectResponse\"\x8a\x01\n\x1bProjectPartialUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08products\x18\x02 \x03(\t\x12\x1e\n\x16_partial_update_fields\x18\x03 \x03(\t\x12\x10\n\x08pub_date\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\r\n\x05owner\x18\x06 \x01(\x05\"]\n\x0eProjectRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08products\x18\x02 \x03(\t\x12\x10\n\x08pub_date\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\r\n\x05owner\x18\x05 \x01(\x05\"^\n\x0fProjectResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08products\x18\x02 \x03(\t\x12\x10\n\x08pub_date\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\r\n\x05owner\x18\x05 \x01(\x05\"$\n\x16ProjectRetrieveRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x32\xcf\x05\n\x15\x42\x61seProductController\x12o\n\x06\x43reate\x12\x30.base_app.products_controller.BaseProductRequest\x1a\x31.base_app.products_controller.BaseProductResponse\"\x00\x12\\\n\x07\x44\x65stroy\x12\x37.base_app.products_controller.BaseProductDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12u\n\x04List\x12\x34.base_app.products_controller.BaseProductListRequest\x1a\x35.base_app.products_controller.BaseProductListResponse\"\x00\x12\x83\x01\n\rPartialUpdate\x12=.base_app.products_controller.BaseProductPartialUpdateRequest\x1a\x31.base_app.products_controller.BaseProductResponse\"\x00\x12y\n\x08Retrieve\x12\x38.base_app.products_controller.BaseProductRetrieveRequest\x1a\x31.base_app.products_controller.BaseProductResponse\"\x00\x12o\n\x06Update\x12\x30.base_app.products_controller.BaseProductRequest\x1a\x31.base_app.products_controller.BaseProductResponse\"\x00\x32\xaa\x05\n\x12\x43\x61tegoryController\x12i\n\x06\x43reate\x12-.base_app.products_controller.CategoryRequest\x1a..base_app.products_controller.CategoryResponse\"\x00\x12Y\n\x07\x44\x65stroy\x12\x34.base_app.products_controller.CategoryDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12o\n\x04List\x12\x31.base_app.products_controller.CategoryListRequest\x1a\x32.base_app.products_controller.CategoryListResponse\"\x00\x12}\n\rPartialUpdate\x12:.base_app.products_controller.CategoryPartialUpdateRequest\x1a..base_app.products_controller.CategoryResponse\"\x00\x12s\n\x08Retrieve\x12\x35.base_app.products_controller.CategoryRetrieveRequest\x1a..base_app.products_controller.CategoryResponse\"\x00\x12i\n\x06Update\x12-.base_app.products_controller.CategoryRequest\x1a..base_app.products_controller.CategoryResponse\"\x00\x32\xe7\x05\n\x17\x43offeeMachineController\x12s\n\x06\x43reate\x12\x32.base_app.products_controller.CoffeeMachineRequest\x1a\x33.base_app.products_controller.CoffeeMachineResponse\"\x00\x12^\n\x07\x44\x65stroy\x12\x39.base_app.products_controller.CoffeeMachineDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12y\n\x04List\x12\x36.base_app.products_controller.CoffeeMachineListRequest\x1a\x37.base_app.products_controller.CoffeeMachineListResponse\"\x00\x12\x87\x01\n\rPartialUpdate\x12?.base_app.products_controller.CoffeeMachinePartialUpdateRequest\x1a\x33.base_app.products_controller.CoffeeMachineResponse\"\x00\x12}\n\x08Retrieve\x12:.base_app.products_controller.CoffeeMachineRetrieveRequest\x1a\x33.base_app.products_controller.CoffeeMachineResponse\"\x00\x12s\n\x06Update\x12\x32.base_app.products_controller.CoffeeMachineRequest\x1a\x33.base_app.products_controller.CoffeeMachineResponse\"\x00\x32\x9e\x05\n\x11LedModeController\x12g\n\x06\x43reate\x12,.base_app.products_controller.LedModeRequest\x1a-.base_app.products_controller.LedModeResponse\"\x00\x12X\n\x07\x44\x65stroy\x12\x33.base_app.products_controller.LedModeDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12m\n\x04List\x12\x30.base_app.products_controller.LedModeListRequest\x1a\x31.base_app.products_controller.LedModeListResponse\"\x00\x12{\n\rPartialUpdate\x12\x39.base_app.products_controller.LedModePartialUpdateRequest\x1a-.base_app.products_controller.LedModeResponse\"\x00\x12q\n\x08Retrieve\x12\x34.base_app.products_controller.LedModeRetrieveRequest\x1a-.base_app.products_controller.LedModeResponse\"\x00\x12g\n\x06Update\x12,.base_app.products_controller.LedModeRequest\x1a-.base_app.products_controller.LedModeResponse\"\x00\x32\xaa\x05\n\x12LedPanelController\x12i\n\x06\x43reate\x12-.base_app.products_controller.LedPanelRequest\x1a..base_app.products_controller.LedPanelResponse\"\x00\x12Y\n\x07\x44\x65stroy\x12\x34.base_app.products_controller.LedPanelDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12o\n\x04List\x12\x31.base_app.products_controller.LedPanelListRequest\x1a\x32.base_app.products_controller.LedPanelListResponse\"\x00\x12}\n\rPartialUpdate\x12:.base_app.products_controller.LedPanelPartialUpdateRequest\x1a..base_app.products_controller.LedPanelResponse\"\x00\x12s\n\x08Retrieve\x12\x35.base_app.products_controller.LedPanelRetrieveRequest\x1a..base_app.products_controller.LedPanelResponse\"\x00\x12i\n\x06Update\x12-.base_app.products_controller.LedPanelRequest\x1a..base_app.products_controller.LedPanelResponse\"\x00\x32\x9e\x05\n\x11ProjectController\x12g\n\x06\x43reate\x12,.base_app.products_controller.ProjectRequest\x1a-.base_app.products_controller.ProjectResponse\"\x00\x12X\n\x07\x44\x65stroy\x12\x33.base_app.products_controller.ProjectDestroyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12m\n\x04List\x12\x30.base_app.products_controller.ProjectListRequest\x1a\x31.base_app.products_controller.ProjectListResponse\"\x00\x12{\n\rPartialUpdate\x12\x39.base_app.products_controller.ProjectPartialUpdateRequest\x1a-.base_app.products_controller.ProjectResponse\"\x00\x12q\n\x08Retrieve\x12\x34.base_app.products_controller.ProjectRetrieveRequest\x1a-.base_app.products_controller.ProjectResponse\"\x00\x12g\n\x06Update\x12,.base_app.products_controller.ProjectRequest\x1a-.base_app.products_controller.ProjectResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'features.products_controller.grpc.products_controller_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BASEPRODUCTDESTROYREQUEST']._serialized_start=122
  _globals['_BASEPRODUCTDESTROYREQUEST']._serialized_end=161
  _globals['_BASEPRODUCTLISTREQUEST']._serialized_start=163
  _globals['_BASEPRODUCTLISTREQUEST']._serialized_end=187
  _globals['_BASEPRODUCTLISTRESPONSE']._serialized_start=189
  _globals['_BASEPRODUCTLISTRESPONSE']._serialized_end=282
  _globals['_BASEPRODUCTPARTIALUPDATEREQUEST']._serialized_start=284
  _globals['_BASEPRODUCTPARTIALUPDATEREQUEST']._serialized_end=395
  _globals['_BASEPRODUCTREQUEST']._serialized_start=397
  _globals['_BASEPRODUCTREQUEST']._serialized_end=463
  _globals['_BASEPRODUCTRESPONSE']._serialized_start=465
  _globals['_BASEPRODUCTRESPONSE']._serialized_end=586
  _globals['_BASEPRODUCTRETRIEVEREQUEST']._serialized_start=588
  _globals['_BASEPRODUCTRETRIEVEREQUEST']._serialized_end=628
  _globals['_CATEGORYDESTROYREQUEST']._serialized_start=630
  _globals['_CATEGORYDESTROYREQUEST']._serialized_end=666
  _globals['_CATEGORYLISTREQUEST']._serialized_start=668
  _globals['_CATEGORYLISTREQUEST']._serialized_end=689
  _globals['_CATEGORYLISTRESPONSE']._serialized_start=691
  _globals['_CATEGORYLISTRESPONSE']._serialized_end=778
  _globals['_CATEGORYPARTIALUPDATEREQUEST']._serialized_start=780
  _globals['_CATEGORYPARTIALUPDATEREQUEST']._serialized_end=868
  _globals['_CATEGORYREQUEST']._serialized_start=870
  _globals['_CATEGORYREQUEST']._serialized_end=913
  _globals['_CATEGORYRESPONSE']._serialized_start=915
  _globals['_CATEGORYRESPONSE']._serialized_end=959
  _globals['_CATEGORYRETRIEVEREQUEST']._serialized_start=961
  _globals['_CATEGORYRETRIEVEREQUEST']._serialized_end=998
  _globals['_COFFEEMACHINEDESTROYREQUEST']._serialized_start=1000
  _globals['_COFFEEMACHINEDESTROYREQUEST']._serialized_end=1041
  _globals['_COFFEEMACHINELISTREQUEST']._serialized_start=1043
  _globals['_COFFEEMACHINELISTREQUEST']._serialized_end=1069
  _globals['_COFFEEMACHINELISTRESPONSE']._serialized_start=1071
  _globals['_COFFEEMACHINELISTRESPONSE']._serialized_end=1168
  _globals['_COFFEEMACHINEPARTIALUPDATEREQUEST']._serialized_start=1171
  _globals['_COFFEEMACHINEPARTIALUPDATEREQUEST']._serialized_end=1428
  _globals['_COFFEEMACHINEREQUEST']._serialized_start=1431
  _globals['_COFFEEMACHINEREQUEST']._serialized_end=1643
  _globals['_COFFEEMACHINERESPONSE']._serialized_start=1646
  _globals['_COFFEEMACHINERESPONSE']._serialized_end=1913
  _globals['_COFFEEMACHINERETRIEVEREQUEST']._serialized_start=1915
  _globals['_COFFEEMACHINERETRIEVEREQUEST']._serialized_end=1957
  _globals['_LEDMODEDESTROYREQUEST']._serialized_start=1959
  _globals['_LEDMODEDESTROYREQUEST']._serialized_end=1994
  _globals['_LEDMODELISTREQUEST']._serialized_start=1996
  _globals['_LEDMODELISTREQUEST']._serialized_end=2016
  _globals['_LEDMODELISTRESPONSE']._serialized_start=2018
  _globals['_LEDMODELISTRESPONSE']._serialized_end=2103
  _globals['_LEDMODEPARTIALUPDATEREQUEST']._serialized_start=2105
  _globals['_LEDMODEPARTIALUPDATEREQUEST']._serialized_end=2192
  _globals['_LEDMODEREQUEST']._serialized_start=2194
  _globals['_LEDMODEREQUEST']._serialized_end=2236
  _globals['_LEDMODERESPONSE']._serialized_start=2238
  _globals['_LEDMODERESPONSE']._serialized_end=2335
  _globals['_LEDMODERETRIEVEREQUEST']._serialized_start=2337
  _globals['_LEDMODERETRIEVEREQUEST']._serialized_end=2373
  _globals['_LEDPANELDESTROYREQUEST']._serialized_start=2375
  _globals['_LEDPANELDESTROYREQUEST']._serialized_end=2411
  _globals['_LEDPANELLISTREQUEST']._serialized_start=2413
  _globals['_LEDPANELLISTREQUEST']._serialized_end=2434
  _globals['_LEDPANELLISTRESPONSE']._serialized_start=2436
  _globals['_LEDPANELLISTRESPONSE']._serialized_end=2523
  _globals['_LEDPANELPARTIALUPDATEREQUEST']._serialized_start=2526
  _globals['_LEDPANELPARTIALUPDATEREQUEST']._serialized_end=2698
  _globals['_LEDPANELREQUEST']._serialized_start=2700
  _globals['_LEDPANELREQUEST']._serialized_end=2827
  _globals['_LEDPANELRESPONSE']._serialized_start=2830
  _globals['_LEDPANELRESPONSE']._serialized_end=3012
  _globals['_LEDPANELRETRIEVEREQUEST']._serialized_start=3014
  _globals['_LEDPANELRETRIEVEREQUEST']._serialized_end=3051
  _globals['_PROJECTDESTROYREQUEST']._serialized_start=3053
  _globals['_PROJECTDESTROYREQUEST']._serialized_end=3088
  _globals['_PROJECTLISTREQUEST']._serialized_start=3090
  _globals['_PROJECTLISTREQUEST']._serialized_end=3110
  _globals['_PROJECTLISTRESPONSE']._serialized_start=3112
  _globals['_PROJECTLISTRESPONSE']._serialized_end=3197
  _globals['_PROJECTPARTIALUPDATEREQUEST']._serialized_start=3200
  _globals['_PROJECTPARTIALUPDATEREQUEST']._serialized_end=3338
  _globals['_PROJECTREQUEST']._serialized_start=3340
  _globals['_PROJECTREQUEST']._serialized_end=3433
  _globals['_PROJECTRESPONSE']._serialized_start=3435
  _globals['_PROJECTRESPONSE']._serialized_end=3529
  _globals['_PROJECTRETRIEVEREQUEST']._serialized_start=3531
  _globals['_PROJECTRETRIEVEREQUEST']._serialized_end=3567
  _globals['_BASEPRODUCTCONTROLLER']._serialized_start=3570
  _globals['_BASEPRODUCTCONTROLLER']._serialized_end=4289
  _globals['_CATEGORYCONTROLLER']._serialized_start=4292
  _globals['_CATEGORYCONTROLLER']._serialized_end=4974
  _globals['_COFFEEMACHINECONTROLLER']._serialized_start=4977
  _globals['_COFFEEMACHINECONTROLLER']._serialized_end=5720
  _globals['_LEDMODECONTROLLER']._serialized_start=5723
  _globals['_LEDMODECONTROLLER']._serialized_end=6393
  _globals['_LEDPANELCONTROLLER']._serialized_start=6396
  _globals['_LEDPANELCONTROLLER']._serialized_end=7078
  _globals['_PROJECTCONTROLLER']._serialized_start=7081
  _globals['_PROJECTCONTROLLER']._serialized_end=7751
# @@protoc_insertion_point(module_scope)
