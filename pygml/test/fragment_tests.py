import pygml
import unittest

class FragmentTests(unittest.TestCase):
    def test_WrongFragmentType(self):
        def should_raise():
            f = pygml.Fragment()
            f.type = 'bull'

        self.assertRaises(ValueError, should_raise)

    def test_RightFragmentType(self):
        try:
            f = pygml.Fragment()
            f.type = 'simple'
        except:
            self.fail()

    def test_FragmentConversion(self):
        f = pygml.Fragment()
        f.add_line('pre', type='pre')
        f.add_line('mid', type='body')
        f.add_line('post', type='post')

        self.assertEqual(str(f), 'pre\nmid\npost')

    def test_FragmentInfix(self):
        f = pygml.Fragment()
        f.add_line('pre', type='pre')
        f.add_line('mid', type='body')
        f.add_line('post', type='post')

        self.assertEqual(f.infix, 'mid')

    def test_SimpleFragment(self):
        f = pygml.SimpleFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('fragment', f.infix)

    def test_InfixFragment(self):
        f = pygml.InfixFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('fragment', f.infix)
