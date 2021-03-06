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

        self.assertEqual(f.infix, '')

    def test_SimpleFragment(self):
        f = pygml.SimpleFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('', f.infix)

    def test_InfixFragment(self):
        f = pygml.InfixFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('fragment', f.infix)
        self.assertFalse(f.body)

    def test_FragmentVariables(self):
        f = pygml.Fragment()
        f.add_fragment(pygml.VariableReturnFragment(name='foo'))
        f.body[0].add_fragment(pygml.VariableReturnFragment(name='bar'))
        f.add_fragment(pygml.VariableReturnFragment(name='buzz'))

        self.assertEqual(['foo', 'bar', 'buzz'], f.variables)
