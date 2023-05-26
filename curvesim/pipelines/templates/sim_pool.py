from abc import ABC, abstractmethod

from curvesim.logging import get_logger

logger = get_logger(__name__)


class SimPool(ABC):
    """
    The interface that must be implemented by pools used in simulations.

    See curvesim.pool.sim_interface for implementations.
    """

    def prepare_for_trades(self, timestamp):
        """
        Does any necessary preparation before computing and doing trades.

        The input timestamp can be used to fetch any auxiliary data
        needed to prep the state.

        Base implementation is a no-op.

        Parameters
        ----------
        timestamp : datetime.datetime
            the time to sample from
        """

    @abstractmethod
    def price(self, coin_in, coin_out, use_fee=True):
        """
        Returns the spot price of `coin_in` quoted in terms of `coin_out`,
        i.e. the ratio of output coin amount to input coin amount for
        an "infinitesimally" small trade.

        Coin IDs should be strings but as a legacy feature integer indices
        corresponding to the pool implementation are allowed (caveat lector).

        The indices are assumed to include base pool underlyer indices.

        Parameters
        ----------
        coin_in : str, int
            ID of coin to be priced; in a swapping context, this is
            the "in"-token.
        coin_out : str, int
            ID of quote currency; in a swapping context, this is the
            "out"-token.
        use_fee: bool, default=False
            Deduct fees.

        Returns
        -------
        float
            Price of `coin_in` quoted in `coin_out`
        """
        raise NotImplementedError

    @abstractmethod
    def trade(self, coin_in, coin_out, size):
        """
        Perform an exchange between two coins.

        Coin IDs should be strings but as a legacy feature integer indices
        corresponding to the pool implementation are allowed (caveat lector).

        Parameters
        ----------
        coin_in : str, int
            ID of "in" coin.
        coin_out : str, int
            ID of "out" coin.
        size : int
            Amount of coin `i` being exchanged.

        Returns
        -------
        (int, int, int)
            (amount of coin `j` received, trading fee, volume)

            Note that coin amounts and fee are in native token units but `volume`
            is normalized to be in the same units as pool value.  This enables
            cross-token comparisons and totaling of volume.
        """
        raise NotImplementedError