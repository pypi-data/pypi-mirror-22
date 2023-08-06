"""
Unittests for Mud base objects

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

import sys
import time
import pathlib
import tempfile
import unittest
from io import StringIO
import tale
from tests.supportstuff import TestDriver, MsgTraceNPC
from tale.base import Location, Exit, Item, Stats, Living
from tale.errors import ActionRefused, ParseError, NonSoulVerb
from tale.accounts import MudAccounts
from tale.player import Player, TextBuffer, PlayerConnection
from tale.parseresult import ParseResult
from tale.tio.console_io import ConsoleIo
from tale.tio.iobase import IoAdapterBase
from tale.charbuilder import CharacterBuilder, valid_playable_race, PlayerNaming
from tale import races, pubsub, mud_context
from tale.demo.story import Story as DemoStory
from tale.story import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        tale.mud_context.driver = TestDriver()
        tale.mud_context.config = StoryConfig()
        tale.mud_context.config.server_mode = GameMode.IF

    def test_init(self):
        player = Player("fritz", "m")
        player.title = "Fritz the great"
        self.assertEqual("fritz", player.name)
        self.assertEqual("Fritz the great", player.title)
        self.assertEqual("", player.description)
        self.assertEqual("human", player.stats.race)
        self.assertEqual("m", player.gender)
        self.assertEqual("m", player.stats.gender)
        self.assertEqual("he", player.subjective)
        self.assertEqual(set(), player.privileges)
        self.assertTrue(1 < player.stats.agi < 100)
        self.assertGreater(player.output_line_delay, 1)
        player.init_gender("f")
        self.assertEqual("f", player.gender)
        self.assertEqual("f", player.stats.gender)
        self.assertEqual("she", player.subjective)

    def test_tell(self):
        player = Player("fritz", "m")
        player.tell(5)
        self.assertEqual(["5\n"], player.test_get_output_paragraphs())
        player.tell("")
        self.assertEqual([], player.test_get_output_paragraphs())
        player.tell("")
        player.tell("")
        self.assertEqual([], player.test_get_output_paragraphs())
        player.tell("")
        player.tell("line1")
        player.tell("line2")
        player.tell("")
        self.assertEqual(["line1\nline2\n"], player.test_get_output_paragraphs())
        player.tell("", format=False)
        player.tell("line1", format=False)
        player.tell("", format=False)
        player.tell("line2", format=False)
        player.tell("", format=False)
        self.assertEqual(["\nline1\n\nline2\n\n"], player.test_get_output_paragraphs())
        player.tell("\n")
        self.assertEqual(["\n"], player.test_get_output_paragraphs())
        player.tell("line1")
        player.tell("line2")
        player.tell("hello\nnewline")
        player.tell("\n")
        player.tell("ints", 42, 999)
        self.assertEqual(["line1\nline2\nhello\nnewline\n", "ints 42 999\n"], player.test_get_output_paragraphs())
        self.assertEqual([], player.test_get_output_paragraphs())
        player.tell("para1", end=False)
        player.tell("para2", end=True)
        player.tell("para3")
        player.tell("\n")
        player.tell("para4", "\n", "para5")
        self.assertEqual(["para1\npara2\n", "para3\n", "para4 \n para5\n"], player.test_get_output_paragraphs())
        player.tell("   xyz   \n  123", format=False)
        self.assertEqual(["   xyz   \n  123\n"], player.test_get_output_paragraphs())
        player.tell("line1", end=True)
        player.tell("\n")
        player.tell("line2", end=True)
        player.tell("\n")
        player.tell("\n")
        self.assertEqual(["line1\n", "\n", "line2\n", "\n", "\n"], player.test_get_output_paragraphs())

    def test_tell_chain(self):
        player = Player("fritz", "m")
        player.tell("hi").tell("there")
        self.assertEqual(["hi\nthere\n"], player.test_get_output_paragraphs())

    def test_tell_emptystring(self):
        player = Player("fritz", "m")
        player.tell("", end=False)
        self.assertEqual([], player.test_get_output_paragraphs())
        player.tell("", end=True)
        self.assertEqual(["\n"], player.test_get_output_paragraphs())
        player.tell("", end=True)
        player.tell("", end=True)
        self.assertEqual(["\n", "\n"], player.test_get_output_paragraphs())

    def test_tell_formats(self):
        player = Player("fritz", "m")
        pc = PlayerConnection(player, ConsoleIo(None))
        player.set_screen_sizes(0, 100)
        player.tell("a b c", format=True)
        player.tell("d e f", format=True)
        self.assertEqual(["a b c\nd e f\n"], player.test_get_output_paragraphs())
        player.tell("a b c", format=True)
        player.tell("d e f", format=True)
        self.assertEqual("a b c d e f\n", pc.get_output())
        player.tell("a b c", format=False)
        player.tell("d e f", format=False)
        self.assertEqual(["a b c\nd e f\n"], player.test_get_output_paragraphs())
        player.tell("a b c", format=False)
        player.tell("d e f", format=False)
        self.assertEqual("a b c\nd e f\n", pc.get_output())
        player.tell("a b c", format=True)
        player.tell("d e f", format=False)
        self.assertEqual(["a b c\n", "d e f\n"], player.test_get_output_paragraphs())
        player.tell("a b c", format=True)
        player.tell("d e f", format=False)
        self.assertEqual("a b c\nd e f\n", pc.get_output())

    def test_tell_formatted(self):
        player = Player("fritz", "m")
        pc = PlayerConnection(player, ConsoleIo(None))
        player.set_screen_sizes(0, 100)
        player.tell("line1")
        player.tell("line2", "\n")
        player.tell("hello\nnewline")
        player.tell("\n")  # paragraph separator
        player.tell("ints", 42, 999)
        self.assertEqual("line1 line2 hello newline\nints 42 999\n", pc.get_output())
        player.tell("para1", end=False)
        player.tell("para2", end=True)
        player.tell("para3")
        player.tell("\n")
        player.tell("para4", "\n", "para5")
        self.assertEqual("para1 para2\npara3\npara4   para5\n", pc.get_output())
        player.tell("word " * 30)
        self.assertNotEqual(("word " * 30).strip(), pc.get_output())
        player.tell("word " * 30, format=False)
        self.assertEqual(("word " * 30) + "\n", pc.get_output())  # when format=False output should be unformatted
        player.tell("   xyz   \n  123", format=False)
        self.assertEqual("   xyz   \n  123\n", pc.get_output())
        player.tell("line1", end=True)
        player.tell("\n")
        player.tell("line2", end=True)
        player.tell("\n")
        player.tell("\n")
        self.assertEqual(["line1\n", "\n", "line2\n", "\n", "\n"], player.test_get_output_paragraphs())
        player.tell("line1", end=True)
        player.tell("\n")
        player.tell("line2", end=True)
        player.tell("\n")
        player.tell("\n")
        self.assertEqual("line1\n\nline2\n\n\n", pc.get_output())

    def test_tell_sep(self):
        player = Player("fritz", "m")
        pc = PlayerConnection(player, ConsoleIo(None))
        player.set_screen_sizes(0, 10)
        player.tell("apple", "bee", "zinc", "rose")
        self.assertEqual(["apple bee zinc rose\n"], player.test_get_output_paragraphs())
        pc.get_output()
        player.tell("apple", "bee", "zinc", "rose", format=False)
        self.assertEqual("apple\nbee\nzinc\nrose\n", pc.get_output())

    def test_look(self):
        player = Player("fritz", "m")
        attic = Location("Attic", "A dark attic.")
        player.look()
        self.assertEqual(["[Limbo]\n", "The intermediate or transitional place or state. There's only nothingness.\nLiving beings end up here if they're not in a proper location yet.\n"], player.test_get_output_paragraphs())
        player.move(attic, silent=True)
        player.look(short=True)
        self.assertEqual(["[Attic]\n"], player.test_get_output_paragraphs())
        julie = Living("julie", "f")
        julie.move(attic, silent=True)
        player.look(short=True)
        self.assertEqual(["[Attic]\n", "Present: julie\n"], player.test_get_output_paragraphs())

    def test_look_brief(self):
        player = Player("fritz", "m")
        attic = Location("Attic", "A dark attic.")
        cellar = Location("Cellar", "A gloomy cellar.")
        julie = Living("julie", "f")
        julie.move(attic, silent=True)
        player.move(attic, silent=True)
        player.brief = 0  # default setting: always long descriptions
        player.look()
        self.assertEqual(["[Attic]\n", "A dark attic.\n", "Julie is here.\n"], player.test_get_output_paragraphs())
        player.look()
        self.assertEqual(["[Attic]\n", "A dark attic.\n", "Julie is here.\n"], player.test_get_output_paragraphs())
        player.look(short=True)   # override
        self.assertEqual(["[Attic]\n", "Present: julie\n"], player.test_get_output_paragraphs())
        player.brief = 1  # short for known, long for new locations
        player.look()
        self.assertEqual(["[Attic]\n", "Present: julie\n"], player.test_get_output_paragraphs())
        player.move(cellar, silent=True)
        player.look()
        self.assertEqual(["[Cellar]\n", "A gloomy cellar.\n"], player.test_get_output_paragraphs())
        player.look()
        self.assertEqual(["[Cellar]\n"], player.test_get_output_paragraphs())
        player.brief = 2  # short always
        player.known_locations.clear()
        player.look()
        self.assertEqual(["[Cellar]\n"], player.test_get_output_paragraphs())
        player.move(attic, silent=True)
        player.look()
        self.assertEqual(["[Attic]\n", "Present: julie\n"], player.test_get_output_paragraphs())
        player.look(short=True)   # override
        self.assertEqual(["[Attic]\n", "Present: julie\n"], player.test_get_output_paragraphs())
        player.look(short=False)  # override
        self.assertEqual(["[Attic]\n", "A dark attic.\n", "Julie is here.\n"], player.test_get_output_paragraphs())

    def test_others(self):
        attic = Location("Attic", "A dark attic.")
        player = Player("merlin", "m")
        player.title = "wizard Merlin"
        julie = MsgTraceNPC("julie", "f", "human")
        fritz = MsgTraceNPC("fritz", "m", "human")
        julie.move(attic, silent=True)
        fritz.move(attic, silent=True)
        player.move(attic, silent=True)
        player.tell_others("one", "two", "three")
        self.assertEqual([], player.test_get_output_paragraphs())
        self.assertEqual(["one", "two", "three"], fritz.messages)
        self.assertEqual(["one", "two", "three"], julie.messages)
        fritz.clearmessages()
        julie.clearmessages()
        player.tell_others("{title} and {Title}")
        self.assertEqual(["wizard Merlin and Wizard Merlin"], fritz.messages)

    def test_wiretap(self):
        attic = Location("Attic", "A dark attic.")
        player = Player("fritz", "m")
        io = ConsoleIo(None)
        io.supports_smartquotes = False
        pc = PlayerConnection(player, io)
        player.set_screen_sizes(0, 100)
        julie = Living("julie", "f")
        julie.move(attic)
        player.move(attic)
        julie.tell("message for julie")
        attic.tell("message for room")
        self.assertEqual(["message for room\n"], player.test_get_output_paragraphs())
        with self.assertRaises(ActionRefused):
            player.create_wiretap(julie)
        player.privileges = {"wizard"}
        player.create_wiretap(julie)
        player.create_wiretap(attic)
        julie.tell("message for julie")
        attic.tell("message for room")
        pubsub.sync()
        output = pc.get_output()
        self.assertTrue("[wiretapped from 'Attic': message for room]" in output)
        self.assertTrue("[wiretapped from 'julie': message for julie]" in output)
        self.assertTrue("[wiretapped from 'julie': message for room]" in output)
        self.assertTrue("message for room " in output)
        # test removing the wiretaps
        player.clear_wiretaps()
        import gc
        gc.collect()
        julie.tell("message for julie")
        attic.tell("message for room")
        self.assertEqual(["message for room\n"], player.test_get_output_paragraphs())

    def test_socialize(self):
        player = Player("fritz", "m")
        attic = Location("Attic", "A dark attic.")
        julie = Living("julie", "f")
        julie.move(attic)
        player.move(attic)
        parsed = player.parse("wave all")
        self.assertEqual("wave", parsed.verb)
        self.assertEqual([julie], parsed.who_order)
        who, playermsg, roommsg, targetmsg = player.soul.process_verb_parsed(player, parsed)
        self.assertEqual({julie}, who)
        self.assertEqual("You wave happily at julie.", playermsg)
        with self.assertRaises(tale.errors.UnknownVerbException):
            player.parse("befrotzificate all and me")
        with self.assertRaises(NonSoulVerb) as x:
            player.parse("befrotzificate all and me", external_verbs={"befrotzificate"})
        parsed = x.exception.parsed
        self.assertEqual("befrotzificate", parsed.verb)
        self.assertEqual([julie, player], parsed.who_order)
        attic.add_exits([Exit("south", "target", "door")])
        try:
            player.parse("push south")
            self.fail("push south should throw a parse error because of the exit that is used")
        except ParseError:
            pass
        with self.assertRaises(NonSoulVerb):
            player.parse("fart south")
        parsed = player.parse("hug julie")
        player.validate_socialize_targets(parsed)

    def test_verbs(self):
        player = Player("julie", "f")
        player.verbs["smurf"] = ""
        self.assertTrue("smurf" in player.verbs)
        del player.verbs["smurf"]
        self.assertFalse("smurf" in player.verbs)

    def test_story_complete(self):
        player = Player("fritz", "m")
        self.assertFalse(player.story_complete)
        player.story_completed()
        self.assertTrue(player.story_complete)

    def test_handle_and_notify_action(self):
        class SpecialPlayer(Player):
            def init(self):
                self.handled = False
                self.handle_verb_called = False
                self.notify_called = False

            def handle_verb(self, parsed, actor):
                self.handle_verb_called = True
                if parsed.verb in self.verbs:
                    self.handled = True
                    return True
                else:
                    return False

            def notify_action(self, parsed, actor):
                self.notify_called = True

        player = SpecialPlayer("julie", "f")
        player.verbs["xywobble"] = ""
        room = Location("room")

        class Chair(Item):
            def init(self):
                self.handled = False
                self.handle_verb_called = False
                self.notify_called = False

            def handle_verb(self, parsed, actor):
                self.handle_verb_called = True
                if parsed.verb in self.verbs:
                    self.handled = True
                    return True
                else:
                    return False

            def notify_action(self, parsed, actor):
                self.notify_called = True

        chair_in_inventory = Chair("littlechair")
        chair_in_inventory.verbs["kerwaffle"] = ""
        player.insert(chair_in_inventory, player)
        chair = Chair("chair")
        chair.verbs["frobnitz"] = ""
        room.init_inventory([player, chair])

        # first check if the handle_verb passes to all objects including inventory
        parsed = ParseResult("kowabungaa12345")
        handled = room.handle_verb(parsed, player)
        self.assertFalse(handled)
        self.assertTrue(chair.handle_verb_called)
        self.assertTrue(player.handle_verb_called)
        self.assertTrue(chair_in_inventory.handle_verb_called)
        self.assertFalse(chair.handled)
        self.assertFalse(player.handled)
        self.assertFalse(chair_in_inventory.handled)

        # check item handling
        player.init()
        chair.init()
        chair_in_inventory.init()
        parsed = ParseResult("frobnitz")
        handled = room.handle_verb(parsed, player)
        self.assertTrue(handled)
        self.assertTrue(chair.handled)
        self.assertFalse(player.handled)
        self.assertFalse(chair_in_inventory.handled)

        # check living handling
        player.init()
        chair.init()
        chair_in_inventory.init()
        parsed = ParseResult("xywobble")
        handled = room.handle_verb(parsed, player)
        self.assertTrue(handled)
        self.assertFalse(chair.handled)
        self.assertTrue(player.handled)
        self.assertFalse(chair_in_inventory.handled)

        # check inventory handling
        player.init()
        chair.init()
        chair_in_inventory.init()
        parsed = ParseResult("kerwaffle")
        handled = room.handle_verb(parsed, player)
        self.assertTrue(handled)
        self.assertFalse(chair.handled)
        self.assertFalse(player.handled)
        self.assertTrue(chair_in_inventory.handled)

        # check notify_action
        player.init()
        chair.init()
        chair_in_inventory.init()
        room.notify_action(parsed, player)
        self.assertTrue(chair.notify_called)
        self.assertTrue(player.notify_called)
        self.assertTrue(chair_in_inventory.notify_called)

    def test_move_notify(self):
        class LocationNotify(Location):
            def notify_npc_left(self, npc, target_location):
                self.npc_left = npc
                self.npc_left_target = target_location

            def notify_npc_arrived(self, npc, previous_location):
                self.npc_arrived = npc
                self.npc_arrived_from = previous_location

            def notify_player_left(self, player: Player, target_location: Location) -> None:
                self.player_left = player
                self.player_left_target = target_location

            def notify_player_arrived(self, player: Player, previous_location: Location) -> None:
                self.player_arrived = player
                self.player_arrived_from = previous_location

        player = Player("julie", "f")
        room1 = LocationNotify("room1")
        room2 = LocationNotify("room2")
        room1.insert(player, player)
        player.move(room2)
        pubsub.sync()
        self.assertEqual(room2, player.location)
        self.assertEqual(player, room1.player_left)
        self.assertEqual(room2, room1.player_left_target)
        self.assertEqual(player, room2.player_arrived)
        self.assertEqual(room1, room2.player_arrived_from)


class TestPlayerConnection(unittest.TestCase):
    def setUp(self):
        tale.mud_context.driver = TestDriver()
        tale.mud_context.config = StoryConfig()
        tale.mud_context.config.server_mode = GameMode.IF

    def test_input(self):
        player = Player("julie", "f")
        with WrappedConsoleIO(None) as io:
            pc = PlayerConnection(player, io)
            player.tell("first this text")
            player.store_input_line("      input text     \n")
            x = pc.input_direct("inputprompt")
            self.assertEqual("input text", x)
            self.assertEqual("  first this text\ninputprompt ", sys.stdout.getvalue())  # should have outputted the buffered text

    def test_peek_output(self):
        player = Player("fritz", "m")
        pc = PlayerConnection(player, ConsoleIo(None))
        player.set_screen_sizes(0, 100)
        player.tell("line1")
        player.tell("line2", 42)
        self.assertEqual(["line1\nline2 42\n"], player.test_peek_output_paragraphs())
        self.assertEqual("line1 line2 42\n", pc.get_output())
        self.assertEqual([], player.test_peek_output_paragraphs())

    def test_write_output(self):
        player = Player("julie", "f")
        with WrappedConsoleIO(None) as io:
            pc = PlayerConnection(player, io)
            player.tell("hello 1", end=True)
            player.tell("hello 2", end=True)
            pc.write_output()
            self.assertEqual("  hello 2", pc.last_output_line)
            self.assertEqual("  hello 1\n  hello 2\n", sys.stdout.getvalue())

    def test_destroy(self):
        pc = PlayerConnection(None, ConsoleIo(None))
        pc.destroy()
        self.assertIsNone(pc.player)
        self.assertIsNone(pc.io)


class TestTextbuffer(unittest.TestCase):
    def test_empty_lines(self):
        output = TextBuffer()
        output.print("")
        output.print("")
        self.assertEqual([], output.get_paragraphs(), "empty strings shouldn't be stored")
        output.print("", format=False)
        output.print("", format=False)
        self.assertEqual([("\n\n", False)], output.get_paragraphs(), "2 empty strings without format should be stored in 1 paragraph with 2 new lines")
        output.print("", end=True)
        output.print("", end=True)
        self.assertEqual([("\n", True), ("\n", True)], output.get_paragraphs(), "2 empty strings with end=true should be stored in 2 paragraphs")
        output.print("", end=True)
        output.print("", end=True)
        output.print("", end=True)
        self.assertEqual([("\n", True), ("\n", True), ("\n", True)], output.get_paragraphs())
        output.print("")
        output.print("1")
        output.print("2")
        output.print("")
        self.assertEqual([("1\n2\n", True)], output.get_paragraphs())

    def test_end(self):
        output = TextBuffer()
        output.print("1", end=True)
        output.print("2", end=True)
        self.assertEqual([("1\n", True), ("2\n", True)], output.get_paragraphs())
        output.print("one")
        output.print("1", end=True)
        output.print("two")
        output.print("2", end=True)
        output.print("three")
        self.assertEqual([("one\n1\n", True), ("two\n2\n", True), ("three\n", True)], output.get_paragraphs())

    def test_whitespace(self):
        output = TextBuffer()
        output.print("1")
        output.print("2")
        output.print("3")
        self.assertEqual([("1\n2\n3\n", True)], output.get_paragraphs())

    def test_strip(self):
        output = TextBuffer()
        output.print("   1   ", format=True)
        self.assertEqual([("1\n", True)], output.get_paragraphs())
        output.print("   1   ", format=False)
        self.assertEqual([("   1   \n", False)], output.get_paragraphs())


class TestCharacterBuilder(unittest.TestCase):
    def setUp(self):
        mud_context.driver = TestDriver()
        mud_context.config = DemoStory().config

    def test_build(self):
        conn = PlayerConnection()
        with WrappedConsoleIO(conn) as io:
            conn.io = io
            b = CharacterBuilder(conn, None)
            builder = b.build_async()
            why, what = next(builder)
            self.assertEqual("input", why)

    def test_validate_race(self):
        self.assertEqual("human", valid_playable_race("human"))
        self.assertEqual("human", valid_playable_race("HUMAN"))
        with self.assertRaises(ValueError):
            valid_playable_race("elemental")
        with self.assertRaises(ValueError):
            valid_playable_race("xyz12343")
        with self.assertRaises(ValueError):
            valid_playable_race("")
        with self.assertRaises(ValueError):
            valid_playable_race(None)

    def test_playernaming(self):
        n = PlayerNaming()
        n.gender = "m"
        n.name = "RINZWIND"
        n.description = "a wizard"
        n.money = 999
        n.stats = Stats.from_race("elemental")
        n.title = "grand master"
        self.assertEqual("rinzwind", n.name)
        p = Player("dummy", "f")
        p.privileges.add("wiz")
        n.apply_to(p)
        self.assertEqual("rinzwind", p.name)
        self.assertEqual("m", p.gender)
        self.assertEqual({"wiz"}, p.privileges)
        self.assertEqual("a wizard", p.description)
        self.assertEqual(999, p.money)
        self.assertEqual("elemental", p.stats.race)
        self.assertEqual("n", p.stats.gender)
        self.assertEqual(races.BodyType.NEBULOUS, p.stats.bodytype)
        self.assertEqual("grand master", p.title)

    def test_idle(self):
        p = Player("dummy", "f")
        c = PlayerConnection(p, WrappedConsoleIO(None))
        self.assertLess(p.idle_time, 0.1)
        self.assertLess(c.idle_time, 0.1)
        time.sleep(0.2)
        self.assertGreater(p.idle_time, 0.1)
        self.assertGreater(c.idle_time, 0.1)
        p.store_input_line("input")
        self.assertLess(p.idle_time, 0.1)
        self.assertLess(c.idle_time, 0.1)


class TestTabCompletion(unittest.TestCase):
    def test_complete_c(self):
        player = Player("fritz", "m")
        driver = TestDriver()
        conn = PlayerConnection(player)
        io = IoAdapterBase(conn)
        conn.io = io
        result = io.tab_complete("c", driver)
        self.assertGreater(len(result), 20)
        self.assertTrue("cackle" in result)
        self.assertTrue("criticize" in result)
        result = io.tab_complete("h", driver)
        self.assertGreater(len(result), 10)
        self.assertTrue("hiss" in result)

    def test_complete_one(self):
        player = Player("fritz", "m")
        driver = TestDriver()
        conn = PlayerConnection(player)
        io = IoAdapterBase(conn)
        conn.io = io
        self.assertEqual(["criticize"], io.tab_complete("critic", driver))


class TestMudAccounts(unittest.TestCase):
    def setUp(self):
        tale.mud_context.driver = TestDriver()
        tale.mud_context.config = StoryConfig()
        tale.mud_context.config.server_mode = GameMode.IF

    def test_accept_name(self):
        self.assertEqual("irm", MudAccounts.accept_name("irm"))
        self.assertEqual("irmendejongyeahz", MudAccounts.accept_name("irmendejongyeahz"))
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("irmendejongyeahxy")   # too long
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("aa")   # too short
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("Irmen")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("irmen de jong")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("irmen_de_jong")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("irmen444")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name(" irmen")
        with self.assertRaises(ValueError):
            MudAccounts.accept_name("irmen ")

    def test_accept_email(self):
        self.assertEqual("x@y", MudAccounts.accept_email("x@y"))
        self.assertEqual("test@some.domain.com", MudAccounts.accept_email("test@some.domain.com"))
        with self.assertRaises(ValueError):
            MudAccounts.accept_email("@")
        with self.assertRaises(ValueError):
            MudAccounts.accept_email("test@")
        with self.assertRaises(ValueError):
            MudAccounts.accept_email("@test.com")
        with self.assertRaises(ValueError):
            MudAccounts.accept_email(" x@y")
        with self.assertRaises(ValueError):
            MudAccounts.accept_email("x@y ")

    def test_accept_password(self):
        pw = "hello3"
        self.assertEqual(pw, MudAccounts.accept_password(pw))
        pw = "hello this is a long pass pharse 12345"
        self.assertEqual(pw, MudAccounts.accept_password(pw))
        pw = "he44zzz"
        self.assertEqual(pw, MudAccounts.accept_password(pw))
        pw = "   test  2  "
        self.assertEqual(pw, MudAccounts.accept_password(pw))
        with self.assertRaises(ValueError):
            MudAccounts.accept_password("")
        with self.assertRaises(ValueError):
            MudAccounts.accept_password("shrt2")
        with self.assertRaises(ValueError):
            MudAccounts.accept_password("no digits")
        with self.assertRaises(ValueError):
            MudAccounts.accept_password("223242455")

    def test_pwhash(self):
        pw, salt = MudAccounts._pwhash("secret")
        pw2, salt2 = MudAccounts._pwhash("secret")
        self.assertNotEqual(pw, pw2)
        self.assertNotEqual(salt, salt2)
        pw, salt = MudAccounts._pwhash("secret", "some salt")
        pw2, salt2 = MudAccounts._pwhash("secret", "some salt")
        self.assertEqual(pw, pw2)
        self.assertEqual(salt, salt2)

    def test_accountcreate_fail(self):
        stats = Stats()
        accounts = MudAccounts(":memory:")
        with self.assertRaises(ValueError):
            accounts.create("testname", "s3cr3t", "test@invalid", stats, {"wizard"})

    def test_dbcreate(self):
        dbfile = pathlib.Path(tempfile.gettempdir()) / "tale_test_accdb_{0:f}.sqlite".format(time.time())
        try:
            accounts = MudAccounts(str(dbfile))
            stats = Stats.from_race("elf", gender='f')
            account = accounts.create("testname", "s3cr3t", "test@invalid", stats, {"wizard"})
            self.assertEqual(60.0, account.stats.weight)
            accs = list(accounts.all_accounts())
            self.assertEqual(1, len(accs))
            account = accs[0]
            self.assertEqual("testname", account.name)
            self.assertEqual({"wizard"}, account.privileges)
            self.assertEqual("f", account.stats.gender)
            self.assertTrue("agi" in account.stats.stat_prios[3])
            self.assertEqual(40, account.stats.agi)
            self.assertEqual(races.BodyType.HUMANOID, account.stats.bodytype)
            self.assertEqual(60.0, account.stats.weight)
            self.assertEqual(races.BodySize.HUMAN_SIZED, account.stats.size)
            self.assertEqual("Edhellen", account.stats.language)
        finally:
            dbfile.unlink()


class WrappedConsoleIO(ConsoleIo):
    def __init__(self, connection: PlayerConnection) -> None:
        super().__init__(connection)

    def __enter__(self):
        self._old_stdout = sys.stdout
        sys.stdout = StringIO()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout


if __name__ == '__main__':
    unittest.main()
